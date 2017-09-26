# encoding: utf-8
from core.model.word_model import WordModel
from core.mongo import Mongodb


class ARPAbetCMUService:
    def __init__(self, config):
        self._mongo = Mongodb(config)
        self._table = 'cmudict'

    def find_one(self, word):
        find_alphabet = self._mongo.find_one(table_name=self._table,
                                             condition={'word': word})
        return WordModel.decode_default(find_alphabet) if find_alphabet else None

    def update(self, model):
        if not model:
            return None
        return self._mongo.update(table_name=self._table,
                                  condition={'word': model.word},
                                  update_data=WordModel.encode_default(model),
                                  upsert=True)