#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
app = Flask(__name__)

from config import current_config

from core.service.arpabet_cmu_dao import ARPAbetCMUService
mongo_service = ARPAbetCMUService(current_config.mongodb)

from core.service.redis_service import RedisService
redis_service = RedisService(current_config.redis)

from webapp.api.crawl_word import crawl_blueprint
app.register_blueprint(crawl_blueprint, url_prefix='/arpabet')
