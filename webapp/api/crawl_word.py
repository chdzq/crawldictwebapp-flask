# encoding: utf-8

import subprocess
from webapp import mongo, redis
from flask import jsonify, request, json
from arpabetandipaconvertor.ipa2arpabet import IPA2ARPAbetConvertor
from core.redis import get_crawl_redis_key, get_rapabet_redis_key
from webapp.exception.generate_worker import generate_custom_error
from webapp.exception.webapp_error import ARPAbetError, SystemError

from logging import getLogger
logger = getLogger(__name__)

from flask.blueprints import Blueprint

crawl_blueprint = Blueprint('crawl', __name__)

@crawl_blueprint.route('/crawl', methods=['POST'])
def crawl_world():
    """
     1.爬虫爬到字
     2.存在redis中
     3.从redis中取
     4.没取到继续下一个爬
     5.最后存在mongodb
     6.返回数据
    """
    body = request.get_json()
    if not body:
        raise generate_custom_error(SystemError.request_param, "body是空")

    body_words = body.get('words', None)
    if not body_words:
        raise generate_custom_error(SystemError.request_param, "参数异常")

    alphabet = None
    spider_names = ["iciba", "iciba", "youdao"]
    spider_param = json.dumps(body_words)
    alphabets = []
    words_dict = {}
    for word in body_words:
        key = get_rapabet_redis_key(word=word)
        alphabet = redis.get_data(key)
        if alphabet:
            alphabets.append({word: alphabet})
            continue
        find_alphabet = mongo.find_one('dict', {'word': word})
        if find_alphabet:
            temp_alphabet = None
            try:
                temp_alphabet = find_alphabet["arpabet"]
            except BaseException as e:
                logger.error(msg=str(e))

            if temp_alphabet:
                alphabets.append({word: temp_alphabet})
                continue
        words_dict[word] = True

    for spider_name in spider_names:
        if not words_dict:
            break
        try:
            subprocess.check_output(['scrapy', 'crawl', spider_name, "-a", "words=" + spider_param])
        except Exception as e:
            logger.error(msg="错误信息 %s" % str(e))
        temp = words_dict.copy()
        for key_word in temp:
            key = get_crawl_redis_key(word=key_word)
            alphabet = redis.get_data(key)
            if alphabet:
                arpabet = None
                try:
                    convert = IPA2ARPAbetConvertor()
                    arpabet = convert.convert(alphabet)
                except Exception as e:
                    raise generate_custom_error(ARPAbetError.ipa_unable_convert_arpabet, "ipa转换arpabet出错")
                mongo.update('dict', {'word': key_word}, {'word': key_word, 'arpabet': arpabet})
                redis.set_data(key=get_rapabet_redis_key(key_word), data=arpabet)
                redis.delete(key=key)
                alphabets.append({key_word: alphabet})
                del words_dict[key_word]

    if not words_dict:
        return jsonify(alphabets)

    raise generate_custom_error(ARPAbetError.unable_crawl_ipa, "只查到了 %s" % jsonify(alphabets))
