"""The Flask App."""

# pylint: disable=broad-except

from flask import Flask, abort, jsonify, request
from rq.job import Job
from rq import Worker, Queue, Connection
from rq import Queue
from .functions import some_long_function
from .redis_resc import redis_conn, redis_queue
import os
app = Flask(__name__)


@app.errorhandler(404)
def resource_not_found(exception):
    """Returns exceptions as part of a json."""
    return jsonify(error=str(exception)), 404


@app.route("/")
def home():
    """Show the app is working."""
    return "Running!"

def count_and_save_words(message):
    return [message]
#add Message
@app.route('/api/message', methods=['PUT', 'POST'])
def addmessaage():
    data = request.get_json()
    message=str(data['Message'])
    q = Queue(connection=redis_conn)
    job = q.enqueue_call(
            func=count_and_save_words, args=(message,), result_ttl=604800)
    return {"url": "/api/message/"+(job.get_id())}

#view Message
@app.route("/api/message/<job_key>", methods=['GET'])
def get_results(job_key):
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
