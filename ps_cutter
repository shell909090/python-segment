#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
import os, sys, time
import segment

def cutfile(filepath):
    cut = segment.get_cutter('frq.db')
    with open(filepath, 'r') as fi: data = fi.read().decode('gbk')
    return list(cut.parse(data))

def frqtrain(filepath):
    db = segment.dictdb('frq.db')
    stat = segment.StatCutter(db, None)
    cut = segment.StringCutter(stat)
    with open(filepath, 'r') as fi: data = fi.read().decode('gbk')
    list(cut.parse(data))
    stat.train()
    db.exporttxt(sys.stdout)

def newtrain(filepath):
    db = segment.dictdb('frq.db')
    new = segment.NewCutter()
    cut = segment.StringCutter(segment.DynamicCutter(db, new))
    with open(filepath, 'r') as fi: data = fi.read().decode('gbk')
    list(cut.parse(data))
    for i in new.wordset:
        print i.encode('utf-8')

def frqstat(filepath):
    frq = {}
    with open(filepath, 'r') as fi: data = fi.read().decode('gbk')
    for i in data:
        if i not in frq: frq[i] = 0
        frq[i] += 1
    print sum(frq.values())
    d = sorted([(k, v) for k, v in frq.items() if v > 10],
               key = lambda x: x[1], reverse = True)
    for k, v in d: print k.encode('utf-8'), v

def main():
    if len(sys.argv) == 1:
        cmds = ['cutshow', 'cut', 'frqtrain', 'newtrain', 'frqstat']
        print '%s [%s]' % (sys.argv[0], '|'.join(cmds))
    elif sys.argv[1] == 'cutshow':
        print '|'.join(cutfile(sys.argv[2])).encode('utf-8')
    elif sys.argv[1] == 'cut': cutfile(sys.argv[2])
    elif sys.argv[1] == 'frqtrain': frqtrain(sys.argv[2])
    elif sys.argv[1] == 'newtrain': newtrain(sys.argv[2])
    elif sys.argv[1] == 'frqstat': frqstat(sys.argv[2])

if __name__ == '__main__': main()
