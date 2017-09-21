# -*- coding: utf-8 -*-

# http://dict.cn/e

from crawlipa.items import CrawlIPAItem
import scrapy
import json

class HaiciName(scrapy.Spider):
    name = "haici"
    allowed_domains = ['dict.cn']
    query_dict_url = 'http://dict.cn/{word}'
    def __init__(self, words, *args, **kwargs):
        super(scrapy.Spider, self).__init__(*args, **kwargs)
        self._words = json.loads(words)

    def start_requests(self):
        for word in self._words:
            request = scrapy.Request(self.query_dict_url.format(word=word), self.parse_dict)
            request.meta['word'] = word
            yield request

    def parse_dict(self, response):
        # content > div.main > div.word > div.phonetic > span:nth-child(2) > bdo
        selectors = response.css('div.word > div.phonetic > span:nth-child(2) > bdo::text').re('.*\[(.*?)\].*?')
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