#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
import os, sys, marshal

class dictdb(object):

    def __init__(self, filepath):
        self.filepath, self.db = filepath, {}
        if filepath: self.loadfile(filepath)

    def save(self, fo): marshal.dump(self.db, fo)
    def load(self, fi): self.db = marshal.load(fi)
    def close(self): self.db = {}
    def sync(self):
        if self.filepath: self.savefile(self.filepath)

    def savefile(self, filepath):
        with open(filepath, 'w') as fo: self.save(fo)

    def loadfile(self, filepath):
        with open(filepath, 'r') as fi: self.load(fi)

    @staticmethod
    def keyhash(u): return u[:2].encode('utf-16')

    def loadtxt(self, filepath):
        with open(filepath, 'r') as fi:
            for line in fi:
                i = line.strip().decode('utf-8').split()
                self.add(i[0], float(i[1]))

    def exporttxt(self, fo):
        for h, vs in self.db.items():
            for k, v in vs.items():
                d = u'%s %f\n' % (h.decode('utf-16') + k, v)
                fo.write(d.encode('utf-8'))

    def reduce(self, factor):
        for h, vs in self.db.items():
            for k, v in vs.items(): vs[k] = v * factor

    def shrink(self, threshold):
        zero = []
        for h, vs in self.db.items():
            self.db[h] = dict([(k, v) for k, v in vs.items()
                               if v > threshold])
            if len(self.db[h]) == 0: zero.append(h)
        for z in zero: del self.db[z]

    def add(self, w, f):
        if len(w) < 2: return
        h = self.keyhash(w)
        d = self.db.setdefault(h, {})
        d[w[2:]] = d.get(w[2:], 0) + f

    def remove(self, w):
        if len(w) < 2: return
        h = self.keyhash(w)
        d = self.db.setdefault(h, {})
        if w[2:] not in d: return
        del d[w[2:]]

    def __getitem__(self, w):
        if len(w) < 2: return 0
        h = self.keyhash(w)
        if h not in self.db: return 0
        return self.db[h].get(w[2:], 0)

    def match(self, sentence):
        if len(sentence) < 2: return
        h, hd, rest = self.keyhash(sentence), sentence[:2], sentence[2:]
        if h not in self.db: return
        d = self.db[h]
        m = []
        for k, v in d.items():
            if rest.startswith(k): m.append((hd + k, v))
        return m
