# encoding: utf-8

import subprocess
from webapp import mongo_service, redis_service
from flask import jsonify, request, json
from arpabetandipaconvertor.phoneticarphabet2arpabet import PhoneticAlphabet2ARPAbetConvertor
from arpabetandipaconvertor.excepts import PhonemeError
from webapp.exception.generate_worker import generate_custom_error
from webapp.exception.webapp_error import ARPAbetError, SystemError
from core.model.word_model import WordModel
from webapp.log.logger import logger
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
    logger.info("收到请求 %s" % str(request))
    body = request.get_json()
    if not body:
        raise generate_custom_error(SystemError.request_param, "body是空")

    body_words = body.get('words', None)
    if not body_words:
        raise generate_custom_error(SystemError.request_param, "参数异常")

    spider_names = ["haici", "iciba", "haiciname"]

    will_crawl_words_dict, alphabets_dict = _work_before_crawl(words=body_words)

    for spider_name in spider_names:
        if not will_crawl_words_dict:
            break
        spider_param = json.dumps([obj for obj in will_crawl_words_dict.keys()])
        try:
            subprocess.check_output(['scrapy', 'crawl', spider_name, "-a", "words=" + spider_param])
        except BaseException as e:
            logger.error(msg="%s 在爬取 %s 时候，执行出错 %s" % (spider_name, spider_param, str(e)))

        _work_after_crawl(will_crawl_words_dict=will_crawl_words_dict,
                          alphabets_dict=alphabets_dict)

    if not will_crawl_words_dict:
        return jsonify(alphabets_dict)

    raise generate_custom_error(error=ARPAbetError.unable_crawl_ipa,
                                message="只查到了部分数据,详细在body里面",
                                data=alphabets_dict)


def _work_before_crawl(words):

    alphabets_dict = {}
    will_crawl_words_dict = {}
    for word in words:
        alphabet = redis_service.get_convert_arpabet(word=word)
        if alphabet:
            alphabets_dict[word] = alphabet
            continue
        find_arpabet = mongo_service.find_one(word=word.upper())
        if find_arpabet:
            temp_arpabet = find_arpabet.get_default_arpabet()
            if temp_arpabet:
                alphabets_dict[word] = temp_arpabet
                redis_service.save_convert_arpabet(find_arpabet)
                continue
        will_crawl_words_dict[word] = True

    return will_crawl_words_dict, alphabets_dict


def _work_after_crawl(will_crawl_words_dict, alphabets_dict):

    temp_will_crawl_words_dict = will_crawl_words_dict.copy()
    for word in temp_will_crawl_words_dict:
        alphabet = redis_service.get_crawl_alphabet(word=word)
        if alphabet:
            word_model = WordModel(word=word)
            try:
                convert = PhoneticAlphabet2ARPAbetConvertor()
                arpabet = convert.convert(alphabet)
                arpabets = WordModel.Arpabets(default=arpabet)
                word_model.arpabets = arpabets
            except PhonemeError as e:
                logger.error(msg="ipa转换arpabet出错: %s" % e.message)
            except BaseException as e:
                logger.error(msg="ipa转换arpabet出错: %s" % str(e))
                continue

            mongo_service.update(model=word_model)
            redis_service.delete_crawl_alphabet(word=word)
            redis_service.save_convert_arpabet(model=word_model)
            alphabets_dict[word] = word_model.get_default_arpabet()
            del will_crawl_words_dict[word]


