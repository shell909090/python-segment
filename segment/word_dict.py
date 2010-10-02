#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-10-01
@author: shell.xu
'''
import sys
import bsddb

def get_tiedlist(key, node, li):
    for k, v in node.items():
        if k == 0: li.append((key, v))
        else: get_tiedlist(key + k, v, li)

class TiedTree(object):
    def __init__(self): self.root = {}
    def load(self, filepath):
        fp = open(filepath, 'r')
        for line in fp:
            line = line.decode('utf-8')
            i = line.split()
            self[i[0]] = int(i[1])
        fp.close()
    # def save(self): self.root.sync()
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

word_dict = TiedTree()

if __name__ == '__main__':
    for k, v in word_dict.match(u'中华人民共和国'):
        print k, v
