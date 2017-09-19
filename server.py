#!/usr/bin/env python
# encoding: utf-8

import subprocess

import uuid
from webapp import app, mongo
from flask import jsonify
from arpabetandipaconvertor.ipa2arpabet import IPA2ARPAbetConvertor

@app.route('/crawl/<string:word>')
def crawl_world(word):
    """
    Run spider in another process and store items in file. Simply issue command:

    > scrapy crawl dmoz -o "output.json"

    wait for  this command to finish, and read output.json to client.
    """
    alphabet_item = None
    spider_names = ["iciba", "youdao"]
    for spider_name in spider_names:
        subprocess.check_output(['scrapy', 'crawl', spider_name, "-a", "word=" + word])
        alphabet_item = mongo.find_one('dict', {"word": word})
        if alphabet_item:
            break

    if alphabet_item:

        if alphabet_item:
            alphabet = alphabet_item["american_phonetic_alphabet"]
            if alphabet:
                convert = IPA2ARPAbetConvertor()
                arpabet = convert.convert(alphabet)
                return jsonify({"result": 0, "data": {"word": word, "arpabet": arpabet}})

    return jsonify({"result": 1000, "data": "查不到"})

if __name__ == '__main__':
    app.run(debug=True)
