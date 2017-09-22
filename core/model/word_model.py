# encoding: utf-8

# "word": "WITH",
# "arpabets": {
#     "default": "W IH1 DH",
#     "random": [
#         "W IH1 TH",
#         "W IH0 TH",
#         "W IH0 DH"
#     ]
# }

class WordModel:

    class Arpabets:

        def __init__(self, default, random=None):
            self._default = default
            self._random = random

        @property
        def default(self):
            return self._default

        @default.setter
        def default(self, default):
            self._default = default

        @property
        def random(self):
            return self._random

        @random.setter
        def random(self, random):
            self._random = random

        # default method for decode
        @staticmethod
        def encode_default(obj):
            if not obj:
                return None
            default = obj.default
            if not default:
                return None
            dic = {"default": default}
            random = obj.random
            if random:
                dic["random"] = random
            return dic

        @staticmethod
        def decode_default(dic):
            if not dic:
                return None

            default = dic.get("default", None)
            if not default:
                return None

            return WordModel.Arpabets(default, dic.get('random'))

    def __init__(self, word, arpabets=None):
        self._word = word
        self._arpabets = arpabets

    @property
    def word(self):
        return self._word

    @property
    def arpabets(self):
        return self._arpabets

    @arpabets.setter
    def arpabets(self, arpabets):
        self._arpabets = arpabets

    def get_default_arpabet(self):
        if self._arpabets:
            return self._arpabets.default
        return None

    # default method for decode
    @staticmethod
    def encode_default(obj):
        if not obj:
            return None
        word = obj.word
        if not word:
            return None
        dic = {"word": word}
        arpabets = WordModel.Arpabets.encode_default(obj.arpabets)
        if arpabets:
            dic["arpabets"] = arpabets
        return dic

    @staticmethod
    def decode_default(dic):
        if not dic:
            return None

        word = dic.get("word", None)
        if not word:
            return None

        arpabets = WordModel.Arpabets.decode_default(dic.get("arpabets", None))
        return WordModel(word=word, arpabets=arpabets)
