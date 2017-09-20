# -*- coding: utf-8 -*-
from crawlipa.items import CrawlIPAItem
import scrapy
import json

class YoudaoSpider(scrapy.Spider):
    name = 'youdao'
    allowed_domains = ['dict.youdao.com']
    query_dict_url = 'http://dict.youdao.com/w/eng/{word}'
    def __init__(self, words, *args, **kwargs):
        super(scrapy.Spider, self).__init__(*args, **kwargs)
        self._words = json.loads(words)

    def start_requests(self):
        for word in self._words:
            request = scrapy.Request(self.query_dict_url.format(word=word), self.parse_dict)
            request.meta['word'] = word
            yield request

    def parse_dict(self, response):
        selectors = response.css('div.baav > span:nth-child(2) > span.phonetic::text').re('.*\[(.*?)\].*?')
        self.logger.info('Parse function called on %s', selectors)
        if selectors:
            item = CrawlIPAItem()
            item["american_phonetic_alphabet"] = selectors[0]
            item["word"] = response.meta['word']
            yield item

