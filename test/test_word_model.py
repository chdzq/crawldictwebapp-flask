# encoding: utf-8
from unittest import TestCase
from core.mongo import Mongodb
from core.model.word_model import WordModel
from flask import json

class TestWordModel(TestCase):
    # "word": "WITH",
    # "arpabets": {
    #     "default": "W IH1 DH",
    #     "random": [
    #         "W IH1 TH",
    #         "W IH0 TH",
    #         "W IH0 DH"
    #     ]
    # }

    def setUp(self):
        self._word_dic = {"word": "WITH",
                          "arpabets":
                              {
                              "default": "W IH1 DH",
                              "random":
                                  [
                                  "W IH1 TH",
                                  "W IH0 TH",
                                  "W IH0 DH"
                                  ]
                              }
                          }
        arpabets = WordModel.Arpabets(default=self._word_dic["arpabets"].get("default"), random=self._word_dic["arpabets"].get("random"))
        self._arpabets = arpabets
        word = WordModel(word=self._word_dic["word"], arpabets=arpabets)
        self._word = word


    def test_encode(self):
        dic = json.loads(json.dumps(self._word, default=WordModel.encode_default))
        self.assertTrue(dic['word'] == self._word_dic['word'])

