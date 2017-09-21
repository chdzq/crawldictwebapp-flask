# -*- coding: utf-8 -*-

# http://ename.dict.cn/Wilkinson

from crawlipa.items import CrawlIPAItem
import scrapy
import json

class HaiciName(scrapy.Spider):
    name = "haiciname"
    allowed_domains = ['ename.dict.cn']
    query_dict_url = 'http://ename.dict.cn/{word}'
    def __init__(self, words, *args, **kwargs):
        super(scrapy.Spider, self).__init__(*args, **kwargs)
        self._words = json.loads(words)

    def start_requests(self):
        for word in self._words:
            request = scrapy.Request(self.query_dict_url.format(word=word), self.parse_dict)
            request.meta['word'] = word
            yield request

    def parse_dict(self, response):
        selectors = response.css('div.forsearch > dt.clearfix> div.fl > em::text').re('.*\[(.*?)\].*?')
        self.logger.info(msg="Parse function called on %s" % str(selectors))
        if selectors:
            american_phonetic_alphabet = selectors[0]
            if not american_phonetic_alphabet:
                return
            american_phonetic_alphabet = american_phonetic_alphabet.replace("ː", ":")
            item = CrawlIPAItem()
            item["american_phonetic_alphabet"] = american_phonetic_alphabet
            item["word"] = response.meta['word']
            yield item
