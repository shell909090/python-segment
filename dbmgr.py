#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
import os, sys, getopt
import segment

dbname = 'frq.db'

def create(filepath):
    ddb = segment.dictdb()
    ddb.loadtxt(filepath)
    ddb.savefile(dbname)

def load(filepath):
    ddb = segment.dictdb(dbname)
    ddb.loadtxt(filepath)
    ddb.sync()

def export(filepath):
    ddb = segment.dictdb(dbname)
    with open(filepath, 'w') as fo: ddb.exporttxt(fo)

def trans_cedict(infile, outfile):
    words = set()
    with open(infile, 'r') as fi:
        for line in fi:
            if line.startswith('#'): continue
            word = line.split()[1].decode('utf-8')
            if len(word) > 1: words.add(word)
    with open(outfile, 'w') as fo:
        for word in list(words):
            fo.write((u'%s 1\n' % word).encode('utf-8'))

def trans_plain(infile, outfile):
    words = set()
    with open(infile, 'r') as fi:
        for line in fi:
            if line.startswith('#'): continue
            word = line.decode('utf-8').strip()
            if len(word) > 1: words.add(word)
    with open(outfile, 'w') as fo:
        for word in list(words):
            fo.write((u'%s 1\n' % word).encode('utf-8'))

def main():
    opts, args = getopt.getopt(sys.argv[1:], 'd:')
    for opt, val in opts:
        if opt == '-d':
            global dbname
            dbname = val
    funcs = ['create', 'load', 'export', 'trans_cedict', 'trans_plain']
    if len(args) == 0:
        print '%s [%s] .. filename' % (sys.argv[0], '|'.join(funcs))
    elif args[0] == 'create': create(args[1])
    elif args[0] == 'load': load(args[1])
    elif args[0] == 'export': export(args[1])
    elif args[0] == 'trans_cedict': trans_cedict(args[1], args[2])
    elif args[0] == 'trans_plain': trans_plain(args[1], args[2])

if __name__ == '__main__': main()
