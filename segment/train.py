#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-17
@author: shell.xu
'''
import os, sys
import dyn, dictdb

class StatCutter(dyn.DynamicCutter):

    def __init__(self, db):
        super(StatCutter, self).__init__(db)
        self.wordfrq = {}

    def parse(self, sentence):
        frq, rslt = self.split(sentence)
        for word, tp in rslt:
            if tp != 0:
                if word not in self.wordfrq: self.wordfrq[word] = 0
                self.wordfrq[word] += 1
            yield word

    def train(self, sync = False):
        for k, v in self.wordfrq.iteritems(): self.db.add(k, v)
        self.db.normalize()
        if sync: self.db.sync()

    def join(self, stat):
        for k, v in stat.wordfrq.iteritems():
            self.wordfrq[k] = self.wordfrq.get(k, 0) + v
        return self

class NewCutter(dyn.DynamicCutter):

    def __init__(self, db):
        super(StatCutter, self).__init__(db)
        self.wordfrq, self.hifrqs = {}, db.hifrqs(40)

    def parse(self, word):
        frq, rslt = self.split(sentence)
        for word, tp in rslt:
            if tp == 0 and len(word) >= 2:
                sp = word.strip(self.hifrqs)
                if len(sp) >= 2:
                    if sp not in self.wordfrq: self.wordfrq[sp] = 0
                    self.wordfrq[sp] += 1
            yield word

    def get_highfrq(self):
        r = sorted(self.wordfrq.items(), key = lambda x: x[1], reverse = True)
        avg = int(float(sum(map(lambda x:x[1], r))) / len(r)) + 1
        return filter(lambda x:x[1]>avg, r)

    def join(self, new):
        for k, v in new.wordfrq.iteritems():
            self.wordfrq[k] = self.wordfrq.get(k, 0) + v
        return self
