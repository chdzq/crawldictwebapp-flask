# encoding: utf-8

class WordItem:

    def __init__(self, word, arpabet):
        self._word = word
        self._arpabet = arpabet

    def set_arpabet(self, arpabet):
        self._arpabet = arpabet
