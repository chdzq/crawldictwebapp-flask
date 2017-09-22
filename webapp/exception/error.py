# encoding: utf-8

class CustomError(Exception):

    def __init__(self, error_code, message, data=None):
        self._error_code = error_code
        self._message = message
        self._data = data

    @property
    def error_code(self):
        return self._error_code

    @property
    def message(self):
        return self._message if self._message else ""

    @property
    def data(self):
        return self._data