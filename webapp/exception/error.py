# encoding: utf-8

class CustomError(Exception):

    def __init__(self, error_code, message):
        self._error_code = error_code
        self._message = message

    def get_error_code(self):
        return self._error_code

    def get_message(self):
        return self._message if self._message else ""