#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
import os, sys
import shelve

class dictdb(object):

    def __init__(self, filepath, flag = 'c'):
        self.db = shelve.open(filepath, flag, 2)

    def flush(self): self.db.sync()

    def close(self): self.db.close()

    @staticmethod
    def keyhash(u):
        return u[:2].encode('utf-16')

    def load(self, fo):
        for line in fo:
            i = line.strip().decode('utf-8').split()
            self.add(i[0], int(i[1]))

    def loadtxt(self, filepath):
        with open(filepath, 'r') as fi: self.load(fi)

    def export(self, fo):
        for h, vs in self.db.items():
            for k, v in vs.items():
                print >>fo, h.decode('utf-16') + k, v

    def add(self, w, f):
        if len(w) < 2: return
        h = self.keyhash(w)
        d = self.db.get(h, {})
        d[w[2:]] = d.get(w[2:], 0) + f
        self.db[h] = d

    def remove(self, w):
        if len(w) < 2: return
        h = self.keyhash(w)
        d = self.db.get(h, {})
        if w[2:] not in d: return
        del d[w[2:]]
        self.db[h] = d

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

if __name__ == '__main__':
    ddb = dictdb('a.db', 'n')
    ddb.loadtxt('../cedict.txt')
    ddb.flush()
