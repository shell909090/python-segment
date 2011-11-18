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

    def join(self, stat):
        for k, v in stat.wordfrq.items():
            self.wordfrq[k] = self.wordfrq.get(k, 0) + v
        return self

HIGHFRQ = u'的我了是不一这个在人来大么有你那就小说们到出\
要着上好然可啊他过后还和为对吧与之'
class NewCutter(object):
    def __init__(self): self.wordfrq = {}

    def parse(self, word):
        if len(word) >= 2:
            for s in xrange(len(word)):
                if word[s] not in HIGHFRQ: break
            for e in xrange(len(word)-1, -1, -1):
                if word[e] not in HIGHFRQ: break
            sp = word[s:e+1]
            if len(sp) >= 2:
                if sp not in self.wordfrq: self.wordfrq[sp] = 0
                self.wordfrq[sp] += 1
        return [word,]

    def get_highfrq(self):
        r = sorted(self.wordfrq.items(), key = lambda x: x[1], reverse = True)
        avg = int(float(sum(map(lambda x:x[1], r))) / len(r)) + 1
        return filter(lambda x:x[1]>avg, r)

    def join(self, new):
        for k, v in new.wordfrq.items():
            self.wordfrq[k] = self.wordfrq.get(k, 0) + v
        return self
