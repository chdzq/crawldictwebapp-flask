#!/usr/bin/env python
# encoding: utf-8

import subprocess

import uuid
from webapp import app, mongo, redis
from flask import jsonify
from arpabetandipaconvertor.ipa2arpabet import IPA2ARPAbetConvertor
from core.redis import get_redis_key

@app.route('/crawl/<string:word>')
def crawl_world(word):
    """
     1.爬虫爬到字
     2.存在redis中
     3.从redis中取
     4.没取到继续下一个爬
     5.最后存在mongodb
     6.返回数据
    """

    alphabet = None
    spider_names = ["youdao", "iciba"]
    key = get_redis_key(word=word)
    for spider_name in spider_names:
        subprocess.check_output(['scrapy', 'crawl', spider_name, "-a", "word=" + word])
        alphabet = redis.get_data(key)
        if alphabet:
            break

    if alphabet:
        convert = IPA2ARPAbetConvertor()
        arpabet = convert.convert(alphabet)
        mongo.update('dict', {'word': word}, alphabet)
        return jsonify({"result": 0, "data": {"word": word, "arpabet": arpabet}})

    return jsonify({"result": 1000, "data": "查不到"})

if __name__ == '__main__':
    app.run(debug=True)
