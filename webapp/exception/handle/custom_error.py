# encoding: utf-8


from flask import make_response, jsonify
from webapp import app
from webapp.exception.error import CustomError
from webapp.exception.generate_worker import get_custom_error_code
from webapp.exception.webapp_error import OtherError
from webapp.model.request_result import RequestResult

from webapp.log.logger import logger

@app.errorhandler(CustomError)
def handle_custom_exception(error):

    logger.error(msg=str(error))

    request_result = RequestResult(result=error.error_code,
                                   message=error.message,
                                   body=error.data)
    response = make_response(jsonify(RequestResult.encode_default(request_result)))
    response.status_code = 200

    return response

@app.errorhandler(Exception)
def handle_exception(error):

    logger.error(msg=str(error))

    request_result = RequestResult(result=get_custom_error_code(error=OtherError.unknow),
                                   message=str(error))
    response = make_response(jsonify(RequestResult.encode_defaultdumps(request_result)))
    response.status_code = 500

    return response

