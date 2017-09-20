# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from core.redis import Redis, get_crawl_redis_key
from config import current_config

class CrawlIPAPipeline:

    def open_spider(self, spider):
        self._redis = Redis(current_config.redis)

    def process_item(self, item, spider):
        alphabet = item['american_phonetic_alphabet']
        if alphabet:
            self._redis.set_data(get_crawl_redis_key(item['word']), item['american_phonetic_alphabet'])
        return item

