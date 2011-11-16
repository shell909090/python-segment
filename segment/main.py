#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-10-01
@author: shell.xu
'''
from word_dict import word_dict
from sp_cut import CutterSpliter
from sp_dyn import DynamicSpliter

class ContPrint(object):
    def parse(self, word, **kargs):
        print word

class ContAll(object):
    def __init__(self): self.rslt = []
    def parse(self, word, **kargs):
        if word: self.rslt.append(word)
    def get_result(self): return self.rslt
    def adjust_dict(self):
        for w in self.rslt:
            if len(w) > 1: word_dict.add_value(w)

