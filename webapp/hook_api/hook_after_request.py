# encoding: utf-8

from flask import make_response, jsonify, json
from webapp import app
from webapp.model.request_result import RequestResult
from webapp.exception.generate_worker import get_custom_error_code
from webapp.exception.webapp_error import OtherError
from webapp.log.logger import logger


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
    encode_request_result = RequestResult.encode_default(request_result)
    new_response = make_response(jsonify(encode_request_result))
    new_response.status_code = response.status_code

    logger.info("%s 正确完成请求,返回 %s" % (response.status_code, encode_request_result))

    return new_response
