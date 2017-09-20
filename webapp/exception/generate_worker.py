# encoding: utf-8

from webapp.exception.error import CustomError
from webapp.exception.webapp_error import *


def get_custom_error_code(error):
    delta = 0
    if isinstance(error, ARPAbetError):
        delta = 1000
    elif isinstance(error, SystemError):
        delta = 9000
    elif isinstance(error, OtherError):
        delta = 8000
    return delta + error.value

def generate_custom_error(error, message):

    return CustomError(error_code=get_custom_error_code(error=error), message=message)