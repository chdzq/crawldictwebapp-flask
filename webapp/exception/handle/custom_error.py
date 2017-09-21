# encoding: utf-8


from flask import make_response, jsonify
from webapp import app
from webapp.exception.error import CustomError
from webapp.exception.generate_worker import get_custom_error_code
from webapp.exception.webapp_error import OtherError

from logging import getLogger
logger = getLogger(__name__)

@app.errorhandler(CustomError)
def handle_custom_exception(error):
    logger.error(msg=str(error))
    error_code = error.get_error_code()
    error_message = error.get_message()

    response = make_response(jsonify({"result": error_code, "message": error_message, "data": ""}))
    response.status_code = 200

    return response

@app.errorhandler(Exception)
def handle_exception(error):
    logger.error(msg=str(error))

    response = make_response(jsonify({
        "result": get_custom_error_code(error=OtherError.unknow),
        "message": str(error), "data": ""
    }))
    response.status_code = 500

    return response

