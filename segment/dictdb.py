#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
import os, sys, math, marshal

class dictdb(object):

    def __init__(self, filepath = None):
        self.close()
        self.filepath = filepath
        if self.filepath: self.loadfile(filepath)

    def save(self, fo):
        marshal.dump((self.db, self.sdb, self.dbs, self.sdbs), fo)
    def load(self, fi):
        self.db, self.sdb, self.dbs, self.sdbs = marshal.load(fi)

    def sync(self):
        if self.filepath: self.savefile(self.filepath)
    def close(self):
        self.db, self.sdb, self.dbs, self.sdbs = {}, {}, None, None

    def savefile(self, filepath):
        with open(filepath, 'w') as fo: self.save(fo)
    def loadfile(self, filepath):
        with open(filepath, 'r') as fi: self.load(fi)

    def importtxt(self, filepath):
        with open(filepath, 'r') as fi:
            for line in fi:
                i = line.strip().decode('utf-8').split()
                if len(i[0]) == 1: self.sdb[i[0]] = float(i[1])
                else: self.add(i[0], float(i[1]))
        self.normalize()

    def exporttxt(self, fo):
        for h, vs in self.db.items():
            for k, v in vs.items():
                d = u'%s %f\n' % (h.decode('utf-16') + k, v)
                fo.write(d.encode('utf-8'))
        for k, v in self.sdb.items():
            fo.write('%s %f\n' % (k.encode('utf-8'), v))

    def normalize(self):
        self.dbs = math.log(sum(self.values()))
        self.sdbs = math.log(sum(self.sdb.values()))

    def gets(self, w):
        return math.log(self.sdb.get(w, 1)) - self.sdbs

    def cals(self, ws):
        return sum(map(self.gets, ws))

    def hifrqs(self):
        return sorted(self.sdb.items(), lambda x:x[1], reverse = True)[40:]

    def items(self):
        for h, vs in self.db.items():
            for k, v in vs.items(): yield h.decode('utf-16') + k, v

    def values(self):
        for vs in self.db.values():
            for i in vs.values(): yield i

    def waterlevel(self, threshold):
        return sum([len([v for v in vs.values() if v >= threshold])
                    for vs in self.db.values()])

    def scale(self, factor):
        for h, vs in self.db.items():
            for k, v in vs.items(): vs[k] = v * factor
        self.normalize()

    def shrink(self, threshold):
        zero = []
        for h, vs in self.db.items():
            self.db[h] = dict([(k, v) for k, v in vs.items()
                               if v >= threshold])
            if len(self.db[h]) == 0: zero.append(h)
        for z in zero: del self.db[z]
        self.normalize()

    def flat(self):
        for h, vs in self.db.items():
            for k, v in vs.items(): vs[k] = 1
        self.normalize()

    def add(self, w, f):
        if len(w) < 2: return
        h = w[:2].encode('utf-16')
        d = self.db.setdefault(h, {})
        d[w[2:]] = d.get(w[2:], 0) + f

    def remove(self, w):
        if len(w) < 2: return
        h = w[:2].encode('utf-16')
        d = self.db.setdefault(h, {})
        if w[2:] not in d: return
        del d[w[2:]]

    def get(self, w):
        if len(w) < 2: return 0
        h = w[:2].encode('utf-16')
        if h not in self.db: return 0
        if w[2:] not in self.db[h]: return 0
        return math.log(self.db[h][w[2:]]) - self.dbs

    def match(self, sentence):
        if len(sentence) < 2: return
        hd, rest = sentence[:2], sentence[2:]
        h = hd.encode('utf-16')
        if h not in self.db: return
        d = self.db[h]
        return [(hd + k, math.log(v) - self.dbs)
                for k, v in d.items() if rest.startswith(k)]
