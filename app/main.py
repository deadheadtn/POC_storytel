"""The Flask App."""

# pylint: disable=broad-except

from flask import Flask, abort, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
from rq.job import Job
from rq import Worker, Queue, Connection
from rq import Queue
from .functions import some_long_function
from .redis_resc import redis_conn, redis_queue
import os
from app import app, db
from app.model.user import Users

@app.errorhandler(404)
def resource_not_found(exception):
    """Returns exceptions as part of a json."""
    return jsonify(error=str(exception)), 404


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Users.query.filter_by(
                public_id=data['public_id']).first()
        except:
            abort(401)

        return f(current_user, *args,  **kwargs)

    return decorator




@app.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()
    if (data['name']==None  or data['password']==None ):
        exception= "Please provide a valid non null name or password"
        abort(404, description=messageError)
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['GET', 'POST'])
def login_user():

  auth = request.authorization

  if not auth or not auth.username or not auth.password:
     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

  user = Users.query.filter_by(name=auth.username).first()

  if check_password_hash(user.password, auth.password):
     token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
     return jsonify({'token' : token.decode('UTF-8')})

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@app.route("/")
def home():
    """Show the app is working."""
    return "Running!"

def count_and_save_words(message):
    return [message]


#add Message
@app.route('/api/message', methods=[ 'POST'])
@token_required
def addmessaage(self):
    data = request.get_json()
    message=str(data['Message'])
    if message==None:
        exception= "Please provide a valid non null message"
        abort(404, description=messageError)
    q = Queue(connection=redis_conn)
    job = q.enqueue_call(
            func=count_and_save_words, args=(message,), result_ttl=604800)
    return {"url": "/api/message/"+(job.get_id())}


#view Message
@app.route("/api/message/<job_key>", methods=['GET'])
@token_required
def get_results(self,job_key):
    job = Job.fetch(str(job_key), connection=redis_conn)
    try:
        if job.is_finished:
            return str(job.result), 200
        else:
            return "Nope!", 202
    except Exception as exception:
        abort(404, description=exception)


if __name__ == "__main__":
    app.run(debug=False)
