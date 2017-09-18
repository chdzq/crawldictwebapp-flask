# -*- coding: utf-8 -*-
from crawlipa.items import CrawlIPAItem
import scrapy

class IcibaSpider(scrapy.Spider):
    name = 'iciba'
    allowed_domains = ['www.iciba.com']
    query_dict_url = 'http://www.iciba.com/{word}'
    def __init__(self, word, *args, **kwargs):
        super(scrapy.Spider, self).__init__(*args, **kwargs)
        self._word = word

    def start_requests(self):
        yield scrapy.Request(self.query_dict_url.format(word=self._word), self.parse_dict)

    def parse_dict(self, response):
        selectors = response.css('div.base-speak > span:nth-child(2) > span::text').re('.*\[(.*?)\].*?')
        self.logger.info('Parse function called on %s', selectors)
        if selectors:
            item = CrawlIPAItem()
            item["american_phonetic_alphabet"] = selectors[0]
            item["word"] = self._word
            yield item

