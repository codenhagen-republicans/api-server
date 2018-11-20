#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://green_api:green_api@localhost/green_api'
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    other_thing = db.Column(db.String(80))

    def __str__(self):
        return str(self.id)

@app.route('/')
def hello_world():
    test = Test(other_thing="Hello world")
    db.session.add(test)
    db.session.commit()
    return str(Test.query.all())


app.run(debug=True)
