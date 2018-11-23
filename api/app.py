#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from google.cloud import translate
import kesko
import json
import csv
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://green_api:green_api@localhost/green_api'
db = SQLAlchemy(app)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'googletranslate.json'
translate_client = translate.Client()

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    other_thing = db.Column(db.String(80))

    def __str__(self):
        return str(self.id)

class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    en_loc = db.Column(db.String(80), nullable=False)
    sv_loc = db.Column(db.String(80), nullable=False)
    co2_impresion = db.Column(db.Float(), nullable=False)
    co2_transport_import = db.Column(db.Float(), nullable=True)

    def __str__(self):
        return str(self.name)


@app.route('/loadcsv')
def load_food():
    source = open('../db/dummy_co2.csv', 'r')
    reader = csv.reader(source)
    line_count = 0
    for row in reader:
        if line_count == 0:
            line_count += 1
        else:
            english = translate_client.translate(row[0], target_language='en')['translatedText']
            swedish = translate_client.translate(row[0], target_language='sv')['translatedText']
            record = Food(name=row[0],en_loc=english,sv_loc=swedish,
                            co2_impresion=float(row[1]),
                            co2_transport_import=(float(row[2]) if row[2] != 'null' else None))
            db.session.add(record)
            db.session.commit()
            line_count += 1
    return 'Load Done'

@app.route('/')
def hello_world():
    test = Test(other_thing="Hello world")
    food = Food.query.first()
    db.session.add(test)
    db.session.commit()
    return str(food.name)

@app.route('/footprint', methods=['GET'])
def footprint():
    ean = request.args.get("ean")
    products = kesko.kesko(ean)

    return json.dumps(products, ensure_ascii=False).encode("utf8")

app.run(debug=True)
