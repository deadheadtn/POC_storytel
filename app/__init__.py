# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2021 - present StoryTel-test-restfull-API
"""

import os

from flask            import Flask
from flask_sqlalchemy import SQLAlchemy

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

#app.config.from_object('app.configuration.Config')

app.config['SECRET_KEY']='77tgFCKJbkKkbKjlhTh1s1ssSsSsSsSsSs3cr3tvOIYR5JH77554##@3'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Setup database
@app.before_first_request
def initialize_database():
    db.create_all()
