#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
from dictdb import dictdb

class DynamicCutter(object):
    DEBUG = False

    def __init__(self, db, next):
        self.db, self.next, self.cache = db, next, {}

    @classmethod
    def cmp_subtree(cls, r1, r2):
        if r1 is None: return True
        if cls.DEBUG: print '+', r1; print '-', r2
        c1 = [len(r) for r, i in r1[1] if i == 0]
        c2 = [len(r) for r, i in r2[1] if i == 0]
        s1, s2 = sum(c1), sum(c2)
        if s1 != s2: return s1 > s2
        s1, s2 = len(r1[1]) - len(c1), len(r2[1]) - len(c2)
        if s1 != s2: return s1 > s2
        return r1[0] < r2[0]

    def rfindc(self, sentence, start_pos = 0):
        for i in xrange(start_pos, len(sentence)):
            cset = self.db.match(sentence[i:])
            if cset: return i, cset
        return -1, []

    def split(self, sentence):
        if sentence not in self.cache:
            self.cache[sentence] = self._split(sentence)
        return self.cache[sentence]

    def _split(self, sentence):
        if not sentence: return 0, []
        if len(sentence) == 1: return self.db.gets(sentence), [(sentence, 0),]

        # looking for the first matches word
        best_rslt = None
        poc, cset = self.rfindc(sentence)
        if poc == -1:
            return (sum(map(self.db.gets, sentence)), [(sentence, 0),])
        pre_cut, rest = sentence[:poc], sentence[poc:]

        # see which of matches is the bast choice
        for c, f in cset:
            r = self.split(rest[len(c):])[:]
            temp_rslt = (f + r[0], [(c, 1),] + r[1])
            if self.cmp_subtree(best_rslt, temp_rslt):
                best_rslt = temp_rslt

        # looking for choices not match in this position
        maxlen = max([len(c) for c, f in cset])
        poc, cset = self.rfindc(rest, 1)
        while poc < maxlen and cset:
            r = self.split(rest[poc:])
            temp_rslt = (self.db.cals(rest[:poc]) + r[0],
                         [(rest[:poc], 0),] + r[1])
            if self.cmp_subtree(best_rslt, temp_rslt):
                best_rslt = temp_rslt
            poc, cset = self.rfindc(rest, poc + 1)

        if pre_cut:
            best_rslt = (self.db.cals(pre_cut) + best_rslt[0],
                         [(pre_cut, 0),] + best_rslt[1])
        if self.DEBUG:
            print '%s => %f %s' % (sentence, best_rslt[0], best_rslt[1])
        return best_rslt

    def parse(self, sentence):
        frq, rslt = self.split(sentence)
        for word, tp in rslt:
            if tp != 0 or not self.next: yield word
            else:
                for i in self.next.parse(word): yield i

    def stop(self): self.cache = {}
