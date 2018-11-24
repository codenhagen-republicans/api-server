#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import requests
import re
import json

def ingredient(overall_weight, raw_ingredient):
    m = re.match(r"(\w+)\s*\(?\s*(\d+[,.]?\d+)?\s*%\s*\)?\s*", raw_ingredient)
    if m is None:
        return None

    name = m.group(1).lower()
    percentage = float(m.group(2).replace(',', '.'))

    return (
        { "name"       : name
        , "weight"     : (overall_weight * percentage / 100)
        , "percentage" : percentage
        })

def ingredients(overall_weight, raw_ingredients):
    return list(
           filter(lambda x: x is not None,
           map(lambda r: ingredient(overall_weight, r),
           raw_ingredients.split(", "))))

def product(json):
    raw_ingredients = json["attributes"]["MATERIAL_V"]["value"]["value"]
    weight = float(json["measurements"]["netWeight"])

    pictures = json["pictureUrls"]
    if not pictures:
        image = None
    else:
        image = pictures[0]["original"]

    return (
        { "name"        : json["labelName"]
        , "image"       : image
        , "weight"      : weight
        , "ingredients" : ingredients(weight, raw_ingredients)
        , "segment"     : json["segment"]
        , "ean"         : json["ean"]
        })

def kesko_request(filters):
    headers = (
        { "Ocp-Apim-Subscription-Key" : "9addf635f65544c49b4a249aec4908c8"
        , "Content-Type"              : "application/json"
        })

    data = { "filters" : filters }

    # API endpoint for Kesko
    kesko_api = "https://kesko.azure-api.net/v1/search/products"

    response = requests.post(kesko_api, headers=headers, json=data)
    return response.json()["results"]

def kesko_segment(segment_id):
    return kesko_request({ "segment" : { "id" : segment_id } })

def kesko_product(ean):
    results = kesko_request({ "ean" : ean })

    if results == []:
        return None
    else:
        return product(results[0])
