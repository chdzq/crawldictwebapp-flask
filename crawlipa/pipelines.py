# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from core.service.redis_service import RedisService
from config import current_config

class CrawlIPAPipeline:

    def open_spider(self, spider):
        self._redis = RedisService(current_config.redis)

    def process_item(self, item, spider):
        alphabet = item['american_phonetic_alphabet']
        if item.get('word') and item.get('american_phonetic_alphabet'):
            self._redis.save_crawl_alphabet(item)
        return item

