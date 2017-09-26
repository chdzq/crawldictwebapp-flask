# encoding: utf-8
from core.model.word_model import WordModel
from core.redis import Redis


def get_crawl_redis_key(word):
    return 'crawl_' + word

def get_rapabet_redis_key(word):
    return 'arpabet_' + word


class RedisService:
    def __init__(self, config):
        self._redis = Redis(redis_config=config)

    def get_convert_arpabet(self, word):
        if not word:
            return None
        key = get_rapabet_redis_key(word=word)
        return self._redis.get_data(key)

    def save_convert_arpabet(self, model):
        if not model:
            return None

        key = get_rapabet_redis_key(word=model.word)
        return self._redis.set_data(key=key,
                                    data=model.get_default_arpabet())

    # 爬回来的音标
    def get_crawl_alphabet(self, word):
        if not word:
            return None
        key = get_crawl_redis_key(word=word)
        return self._redis.get_data(key)

    # 爬回来的音标
    def save_crawl_alphabet(self, model):
        if not model:
            return None
        key = get_crawl_redis_key(word=model.get("word"))
        return self._redis.set_data(key=key,
                                    data=model.get("american_phonetic_alphabet"))

    def delete_crawl_alphabet(self, word):
        if not word:
            return None
        key = get_crawl_redis_key(word=word)
        return self._redis.delete(key=key)
