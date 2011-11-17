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

    def __init__(self): self.wordfrq = {}

    def parse(self, word):
        if len(word) >= 3:
            sp = word
            while sp[0] in self.HIGHFRQ or sp[-1] in self.HIGHFRQ:
                if sp[0] in self.HIGHFRQ: del sp[0]
                if sp[-1] in self.HIGHFRQ: del sp[-1]
            if not any([(c in sp) for c in self.HIGHFRQ]):
                if sp not in self.wordfrq: self.wordfrq[sp] = 0
                self.wordfrq[sp] += 1
        return [word,]

    def get_highfrq(self):
        r = sorted(self.wordfrq.items(), key = lambda x: x[1])
        return r[len(r)/10:]
