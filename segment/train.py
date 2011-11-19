#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-17
@author: shell.xu
'''
import os, sys
import dyn, dictdb

class StatCutter(dyn.DynamicCutter):

    def __init__(self, db, next):
        super(StatCutter, self).__init__(db, next)
        self.wordfrq = {}

    def parse(self, sentence):
        frq, rslt = self.split(sentence)
        for word, tp in rslt:
            if tp != 0:
                if word not in self.wordfrq: self.wordfrq[word] = 0
                self.wordfrq[word] += 1
                yield word
            elif not self.next: yield word
            else:
                for i in self.next.parse(word): yield i

    def train(self, sync = False):
        for k, v in self.wordfrq.items(): self.db.add(k, v)
        self.db.normalize()
        if sync: self.db.sync()

    def join(self, stat):
        for k, v in stat.wordfrq.items():
            self.wordfrq[k] = self.wordfrq.get(k, 0) + v
        return self

class NewCutter(object):
    def __init__(self, db):
        self.wordfrq, self.hifrqs = {}, db.hifrqs()

    def parse(self, word):
        if len(word) >= 2:
            for s in xrange(len(word)):
                if word[s] not in self.hifrqs: break
            for e in xrange(len(word)-1, -1, -1):
                if word[e] not in self.hifrqs: break
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
