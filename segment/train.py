#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-17
@author: shell.xu
'''
import os, sys
import dyn

class StatCutter(dyn.DynamicCutter):

    def __init__(self, db, next):
        super(StatCutter, self).__init__(db, next)
        self.wordfrq = {}

    def parse(self, sentence):
        for word, frq in self.split(sentence):
            if frq != 0:
                if word not in self.wordfrq: self.wordfrq[word] = 0
                self.wordfrq[word] += 1
                yield word
            elif not self.next: yield word
            else:
                for i in self.next.parse(word): yield i

    def train(self, sync = False):
        for k, v in self.wordfrq.items(): self.db.add(k, v)
        if sync: self.db.sync()

class NewCutter(object):
    HIGHFRQ = u'的我了是不一这个在人来大么有你那就小说们到出要着上好然可啊他过后还和'

    def __init__(self): self.wordset = set()

    def parse(self, word):
        if len(word) >= 3:
            if not any([(c in word) for c in self.HIGHFRQ]):
                self.wordset.add(word)
        return [word,]
