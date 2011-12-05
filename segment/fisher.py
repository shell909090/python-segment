#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-15
@author: shell.xu
'''
import os, sys, math, marshal
import unicodedata
from dbase import dbase, readfile_cd

def fixinit(mid):
    def getfunc(func):
        return lambda *p: (func(*p) + mid) / 2
    return getfunc

class Fisher(dbase):
    FORBIDDEN = set(['Pd', 'Nd'])

    def save(self, fo): marshal.dump(self.freq, fo)
    def load(self, fi): self.freq = marshal.load(fi)

    def close(self): self.freq = {}

    def set_segment(self, segfunc):
        self.segfunc = segfunc

    def add(self, terms, cls):
        for t in terms:
            frq = self.freq.setdefault(t, {})
            if cls not in frq: frq[cls] = 0
            frq[cls] += 1

    def remove(self, terms, cls):
        for t in terms: self.freq[t][cls] -= 1

    @staticmethod
    def invchi2(chi, df):
        m = chi / 2.0
        s = term = math.exp(-m)
        for i in xrange(1, df//2):
            term *= m / i
            s += term
        return min(s, 1)

    @fixinit(0.5)
    def cprob(self, t, cls):
        if t not in self.freq: return 0
        frq = self.freq[t]
        return float(frq.get(cls, 0)) / sum(frq.values())

    def prob(self, terms, cls):
        fs = sum(map(lambda t: math.log(self.cprob(t, cls)),
                     terms))
        return self.invchi2(-2 * fs, len(terms) * 2)

    def proc_text(self, data):
        r = set()
        fdbfunc = lambda x: unicodedata.category(x) in self.FORBIDDEN
        for t in self.segfunc(data):
            if len(t) < 2: continue
            if any(map(fdbfunc, t)): continue
            r.add(t)
        return r

    def train(self, data, cls): self.add(self.proc_text(data), cls)

    def trainfile(self, filepath, cls):
        print 'process', cls, filepath
        return self.train(readfile_cd(filepath), cls)

    def classify(self, data, clses):
        terms = self.proc_text(data)
        for cls in clses:
            print '\t', cls, self.prob(terms, cls)

    def classifyfile(self, filepath, clses):
        print 'classify', filepath
        return self.classify(readfile_cd(filepath), clses)
