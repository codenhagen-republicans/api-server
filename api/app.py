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

class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    co2_impresion = db.Column(db.Float(), nullable=False)
    co2_transport_import = db.Column(db.Float(), nullable=True)

    def __str__(self):
        return str(self.name)

@app.route('/')
def hello_world():
    test = Test(other_thing="Hello world")
    food = Food.query.first()
    db.session.add(test)
    db.session.commit()
    return str(food.name)


app.run(debug=True)
