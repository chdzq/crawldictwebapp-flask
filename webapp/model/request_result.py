# encoding: utf-8

class RequestResult:

    def __init__(self, result=0, body = None, message = None):
        self._result = result
        self._body = body
        self._message = message

    @property
    def result(self):
        return self._result

    @property
    def body(self):
        return self._body

    @property
    def message(self):
        return self._message

    # default method for decode
    @staticmethod
    def encode_default(obj):

        if not isinstance(obj, RequestResult):
            return None
        dic = {"result": obj.result}

        body = obj.body
        if body:
            dic["body"] = body

        message = obj.message
        if message:
            dic["message"] = message

        return dic

    @staticmethod
    def decode_default(obj):

        if not obj:
            return None
        result = obj.get("result")
        if result is None:
            return None

        return RequestResult(result=result,
                             body=obj.get("body"),
                             message=obj.get("message"))

