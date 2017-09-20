# encoding: utf-8
from redis.exceptions import RedisError
from webapp import app
from logging import getLogger
from flask import make_response, jsonify
from webapp.exception.generate_worker import get_custom_error_code
from webapp.exception.webapp_error import SystemError

logger = getLogger(__name__)

@app.errorhandler(RedisError)
def handle_redis_exception(error):
    message = "Redis error: %s" % str(error)
    logger.error(msg=message)
    response = make_response(jsonify({
        "result": get_custom_error_code(error=SystemError.redis),
        "message": message, "data": ""
    }))
    response.status_code = 500

    return response