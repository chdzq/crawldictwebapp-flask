# encoding: utf-8

import subprocess
from webapp import app, mongo, redis
from flask import jsonify, make_response
from arpabetandipaconvertor.ipa2arpabet import IPA2ARPAbetConvertor
from core.redis import get_redis_key
from webapp.exception.generate_worker import generate_custom_error
from webapp.exception.webapp_error import ARPAbetError


@app.route('/arpabet/crawl/<string:word>')
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
    spider_names = ["youdao", "iciba", "youdao"]
    key = get_redis_key(word=word)
    for spider_name in spider_names:
        subprocess.check_output(['scrapy', 'crawl', spider_name, "-a", "word=" + word])
        alphabet = redis.get_data(key)
        if alphabet:
            break

    if alphabet:
        arpabet = None
        try:
            convert = IPA2ARPAbetConvertor()
            arpabet = convert.convert(alphabet)
        except Exception as e:
            raise generate_custom_error(ARPAbetError.ipa_unable_convert_arpabet, "ipa转换arpabet出错")
        mongo.update('dict', {'word': word}, {'word': word, 'arpabet': arpabet})
        return jsonify({"result": 0, "data": {"word": word, "arpabet": arpabet}})

    raise generate_custom_error(ARPAbetError.unable_crawl_ipa, "查不到" + word + "的ipa")
