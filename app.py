#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import kesko
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
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

def compute_footprint(foods, ingredients):
    total_footprint = 0

    for ingredient in ingredients:
        for food in foods:
            if food.name == ingredient["name"]:
                footprint = food.co2_impresion * ingredient["weight"]
                total_footprint += footprint
                ingredient["footprint"] = footprint

    return total_footprint

@app.route('/footprint', methods=['GET'])
def footprint():
    ean = request.args.get("ean")
    products = kesko.kesko(ean)

    for product in products:
        ingredient_names = (ingredient["name"] for ingredient in product["ingredients"])
        foods = db.session.query(Food).filter(Food.name.in_(ingredient_names)).all()
        product["footprint"] = compute_footprint(foods, product["ingredients"])

    return json.dumps(products, ensure_ascii=False).encode("utf8")

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
