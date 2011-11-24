#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
import math, marshal
from dbase import dbase

class dictdb(dbase):

    def save(self, fo):
        marshal.dump((self.db, self.sdb, self.dbs, self.sdbs), fo)
    def load(self, fi):
        self.db, self.sdb, self.dbs, self.sdbs = marshal.load(fi)

    def close(self):
        self.db, self.sdb, self.dbs, self.sdbs = {}, {}, None, None

    def importtxt(self, filepath):
        with open(filepath, 'r') as fi:
            for line in fi:
                i = line.strip().decode('utf-8').split()
                if len(i[0]) == 1: self.sdb[i[0]] = float(i[1])
                else: self.add(i[0], float(i[1]))
        self.normalize()

    def exporttxt(self, fo):
        for h, vs in self.db.iteritems():
            for k, v in vs.iteritems():
                d = u'%s %f\n' % (h + k, v)
                fo.write(d.encode('utf-8'))
        for k, v in self.sdb.iteritems():
            fo.write('%s %f\n' % (k.encode('utf-8'), v))

    def normalize(self):
        self.dbs = math.log(sum(self.values()))
        self.sdbs = math.log(sum(self.sdb.values()))

    def gets(self, w):
        return math.log(self.sdb.get(w, 1)) - self.sdbs

    def cals(self, ws):
        return sum(map(self.gets, ws))

    def hifrqs(self, num):
        return sorted(self.sdb.items(), lambda x:x[1], reverse = True)[num:]

    def items(self):
        for h, vs in self.db.iteritems():
            for k, v in vs.iteritems(): yield h + k, v

    def values(self):
        for vs in self.db.values():
            for i in vs.values(): yield i

    def add(self, w, f):
        if len(w) < 2: return
        h, r = w[:2], w[2:]
        d = self.db.setdefault(h, {})
        d[r] = d.get(r, 0) + f

    def remove(self, w):
        if len(w) < 2: return
        h, r = w[:2], w[2:]
        d = self.db.setdefault(h, {})
        if r not in d: return
        del d[r]

    def get(self, w):
        if len(w) < 2: return 0
        h, r = w[:2], w[2:]
        if h not in self.db: return 0
        if r not in self.db[h]: return 0
        return math.log(self.db[h][r]) - self.dbs

    def match(self, sentence):
        if len(sentence) < 2: return
        h, r = sentence[:2], sentence[2:]
        if h not in self.db: return
        return [(h + k, math.log(v) - self.dbs)
                for k, v in self.db[h].iteritems() if r.startswith(k)]
