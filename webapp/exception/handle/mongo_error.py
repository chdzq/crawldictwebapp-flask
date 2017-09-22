from pymongo.errors import PyMongoError
from webapp import app
from logging import getLogger
from flask import make_response, jsonify
from webapp.exception.generate_worker import get_custom_error_code
from webapp.exception.webapp_error import SystemError
from webapp.model.request_result import RequestResult

logger = getLogger(__name__)

@app.errorhandler(PyMongoError)
def handle_mongo_exception(error):

    message = "Mongodb error: %s" % str(error)
    logger.error(msg=message)
    request_result = RequestResult(result=get_custom_error_code(error=SystemError.mongo_db),
                                   message=message)
    response = make_response(jsonify(RequestResult.encode_default(request_result)))
    response.status_code = 500

    return response