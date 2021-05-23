# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2021 - present StoryTel-test-restfull-API
"""

import os

from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

#app.config.from_object('app.configuration.Config')


"""
Setting up the basic secret and db conf

"""
app.config['SECRET_KEY']='77tgFCKJbkKkbKjlhTh1s1ssSsSsSsSsSs3cr3tvOIYR5JH77554##@3'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CSRF_ENABLED'] = True

"""
Setting up the limiter default limit rate

"""

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute"]
)

db = SQLAlchemy(app)
# Setup database
@app.before_first_request
def initialize_database():
    db.create_all()
