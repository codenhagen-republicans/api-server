#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException

import kesko
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)

app.config['BASIC_AUTH_USERNAME'] = "admin"
app.config['BASIC_AUTH_PASSWORD'] = os.environ["BASIC_AUTH_PASSWORD"]
admin = Admin(app)
basic_auth = BasicAuth(app)


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    other_thing = db.Column(db.String(80))

    def __str__(self):
        return str(self.id)

class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    co2_impresion = db.Column(db.Float(), nullable=False)
    co2_transport_import = db.Column(db.Float(), nullable=True)

    def __str__(self):
        return str(self.name)

class Footprint(db.Model):
    __tablename__ = 'footprint'

    id = db.Column(db.Integer, primary_key=True)
    ean = db.Column(db.Text, nullable=False)
    co2 = db.Column(db.Float(), nullable=False)

    def __str__(self):
        return str(self.ean)

@app.route('/')
def hello_world():
    test = Test(other_thing="Hello world")
    food = Food.query.first()
    db.session.add(test)
    db.session.commit()
    return str(food.name)

def footprint_ingredients(foods, ingredients):
    total_footprint = 0

    for food in foods:
        for ingredient in ingredients:
            if food.name == ingredient["name"]:
                footprint = food.co2_impresion * ingredient["weight"]
                total_footprint += footprint
                ingredient["footprint"] = footprint

    return total_footprint

def footprint_product(product):
    footprint = db.session.query(Footprint).filter(Footprint.ean == product["ean"]).all()

    if footprint == []:
        # If not present, compute the footprint from the ingredients
        ingredient_names = (ingredient["name"] for ingredient in product["ingredients"])
        foods = db.session.query(Food).filter(Food.name.in_(ingredient_names)).all()
        product["footprint"] = footprint_ingredients(foods, product["ingredients"])
    else:
        product["footprint"] = footprint[0].co2

@app.route('/footprint', methods=['GET'])
def footprint():
    ean = request.args.get("ean")
    product = kesko.kesko_product(ean)

    if product == None:
        return "null"

    # Products in the same segment
    segment_products = list(map(kesko.product, kesko.kesko_segment(product["segment"]["id"])))

    # Add footprint information
    footprint_product(product)

    for p in segment_products:
        footprint_product(p)

    recommendation = min(segment_products, key=lambda p: p["footprint"])

    output = (
        { "product" : product
        , "recommendation" : recommendation
        })

    return json.dumps(output, ensure_ascii=False).encode("utf8")

admin.add_view(ModelView(Food, db.session))
admin.add_view(ModelView(Footprint, db.session))

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=True)
