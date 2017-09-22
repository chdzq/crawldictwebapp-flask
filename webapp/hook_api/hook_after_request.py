# encoding: utf-8

from flask import make_response, jsonify, json
from webapp import app
from webapp.model.request_result import RequestResult
from webapp.exception.generate_worker import get_custom_error_code
from webapp.exception.webapp_error import OtherError


@app.after_request
def handle_after(response):

    # 200~<300范围内的响应
    data = json.loads(response.get_data())
    result = RequestResult.decode_default(data)
    if result:
        return response

    is_ok = int(response.status_code / 200)
    request_result = RequestResult(result=0 if is_ok else get_custom_error_code(error=OtherError.unknow),
                                   body=data)
    new_response = make_response(jsonify(RequestResult.encode_default(request_result)))
    new_response.status_code = response.status_code

    return new_response