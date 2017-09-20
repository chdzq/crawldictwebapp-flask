# -*- coding: utf-8 -*-
from crawlipa.items import CrawlIPAItem
import scrapy
import json

class IcibaSpider(scrapy.Spider):
    name = 'iciba'
    allowed_domains = ['www.iciba.com']
    query_dict_url = 'http://www.iciba.com/{word}'
    def __init__(self, words, *args, **kwargs):
        super(scrapy.Spider, self).__init__(*args, **kwargs)
        self._words = json.loads(words)

    def start_requests(self):
        for word in self._words:
            request = scrapy.Request(self.query_dict_url.format(word=word), self.parse_dict)
            request.meta['word'] = word
            yield request

    def parse_dict(self, response):
        selectors = response.css('div.base-speak > span:nth-child(2) > span::text').re('.*\[(.*?)\].*?')
        self.logger.info(msg="Parse function called on %s" % str(selectors))
        if selectors:
            item = CrawlIPAItem()
            item["american_phonetic_alphabet"] = selectors[0]
            item["word"] = response.meta['word']
            yield item

