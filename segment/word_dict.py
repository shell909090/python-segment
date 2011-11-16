#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-10-01
@author: shell.xu
'''
from __future__ import with_statement
import sys
import cPickle

def get_tiedlist(key, node, li):
    for k, v in node.items():
        if k == 0: li.append((key, v))
        else: get_tiedlist(key + k, v, li)

class TiedTree(object):
    def __init__(self): self.root = {}
    def load_text(self, filepath):
        with open(filepath, 'r') as fp:
            for line in fp:
                i = line.decode('utf-8').split()
                self[i[0]] = int(i[1])
    def save_text(self, filepath):
        with open(filepath, 'w') as fp:
            f = lambda k, v: fp.write((u'%s %d\n' % (k, v)).encode('utf-8'))
            self.get_all(f)
    def load_pick(self, filepath):
        with open(filepath, 'rb') as fp: self.root = cPickle.load(fp)
    def save_pick(self, filepath):
        with open(filepath, 'wb') as fp: cPickle.dump(self.root, fp, -1)
    def __setitem__(self, key, value):
        n = self.root
        for k in key:
            if k not in n: n[k] = {}
            n = n[k]
        n[0] = value
    def __getitem__(self, key):
        n, li = self.root, []
        for k in key:
            if k not in n: return []
            n = n[k]
        get_tiedlist(key, n, li)
        return li
    def match(self, sentence):
        key, n, li = '', self.root, []
        for i, k in enumerate(sentence):
            if k not in n: return li
            n = n[k]
            if 0 in n: li.append((sentence[:i + 1], n[0]))
        return li
    def add_value(self, key, value = 1):
        n = self.root
        for k in key:
            if k not in n: return False
            n = n[k]
        n[0] += value
        return True
    def get_all(self, func, node = None, key = u''):
        if not node: node = self.root
        if 0 in node: func(key, node[0])
        for k, v in node.items():
            if k != 0: self.get_all(func, v, key + k)

word_dict = TiedTree()

if __name__ == '__main__':
    word_dict.load_text('cedict.txt')
    word_dict.save_pick('cedict.pick')

