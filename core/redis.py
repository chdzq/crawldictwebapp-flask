#!/usr/bin/env python
# encoding: utf-8

from redis import StrictRedis
import pickle

class Redis:

    def __init__(self, redis_config):
        host = redis_config.get('host')
        port = redis_config.get('port')
        db = redis_config.get('db')

        r = StrictRedis(host=host, port=port, db=db)
        self._redis = r

    '''
    将内存数据二进制通过序列号转为文本流，再存入redis
    '''
    def set_data(self, key, data, ex=None):
        self._redis.set(key, pickle.dumps(data), ex)

    '''
    将文本流从redis中读取并反序列化，返回返回
    '''
    def get_data(self, key):
        data = self._redis.get(key)
        if data is None:
            return None
        return pickle.loads(data)

    def delete(self, key):
        return self._redis.delete(key)
