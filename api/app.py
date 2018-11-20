#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'


app.run(debug=True)
