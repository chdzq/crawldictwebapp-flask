# encoding: utf-8
from redis.exceptions import RedisError
from webapp import app
from flask import make_response, jsonify
from webapp.exception.generate_worker import get_custom_error_code
from webapp.exception.webapp_error import SystemError
from webapp.model.request_result import RequestResult
from webapp.log.logger import logger


@app.errorhandler(RedisError)
def handle_redis_exception(error):

    message = "Redis error: %s" % str(error)
    logger.error(msg=message)
    request_result = RequestResult(result=get_custom_error_code(error=SystemError.redis),
                                   message=message)
    response = make_response(jsonify(RequestResult.encode_default(request_result)))
    response.status_code = 500

    return response