# encoding: utf-8

from flask import make_response, jsonify, json
from webapp import app

@app.after_request
def handle_after(response):
    if 1 == int(response.status_code/200): #200~<300范围内的响应
         new_response = make_response(jsonify({"result": 0, "body": json.loads(response.get_data())}))
         new_response.status_code = response.status_code
         return new_response
    return response