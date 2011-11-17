#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
from dictdb import dictdb

class DynamicCutter(object):
    def __init__(self, db, next):
        self.db, self.next, self.cache = db, next, {}

    @staticmethod
    def cmp_subtree(r1, r2):
        if r1 is None: return True
        c1 = [len(r) for r, i in r1 if i == 0]
        c2 = [len(r) for r, i in r2 if i == 0]
        s1, s2 = sum(c1), sum(c2)
        if s1 != s2: return s1 > s2
        s1, s2 = len(r1) - len(c1), len(r2) - len(c2)
        if s1 != s2: return s1 > s2
        return sum([r[1] for r in r1]) < sum([r[1] for r in r2])

    def rfindc(self, sentence, start_pos = 0):
        for i in xrange(start_pos, len(sentence)):
            cset = self.db.match(sentence[i:])
            if cset: return i, cset
        return 0, []

    def split(self, sentence):
        if sentence not in self.cache:
            self.cache[sentence] = self._split(sentence)
        return self.cache[sentence]

    def _split(self, sentence):
        if not sentence: return []
        if len(sentence) < 2: return [(sentence, 0),]

        best_rslt = None
        poc, cset = self.rfindc(sentence)
        if poc == 0: pre_cut, rest = None, sentence
        else: pre_cut, rest = sentence[:poc], sentence[poc:]

        for c, f in cset:
            temp_rslt = [(c, f),] + self.split(rest[len(c):])
            if self.cmp_subtree(best_rslt, temp_rslt):
                best_rslt = temp_rslt

        if not cset: maxlen = len(rest)
        else: maxlen = max([len(c) for c, f in cset])
        poc, cset = self.rfindc(rest, 1)
        while poc < maxlen and cset:
            temp_rslt = [(rest[:poc], 0),] + self.split(rest[poc:])
            if self.cmp_subtree(best_rslt, temp_rslt):
                best_rslt = temp_rslt
            poc, cset = self.rfindc(rest, poc + 1)

        if best_rslt is None: best_rslt = [(rest, 0),]
        if pre_cut: best_rslt.insert(0, (pre_cut, 0))
        # print '%s => %s' % (sentence, best_rslt)
        return best_rslt

    def parse(self, sentence):
        for word, frq in self.split(sentence):
            if frq != 0 or not self.next: yield word
            else:
                for i in self.next.parse(word): yield i

    def stop(self): self.cache = {}
