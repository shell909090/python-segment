#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-10-01
@author: shell.xu
'''
import sys

words = set()

if __name__ == '__main__':
    infile = open(sys.argv[1], 'r')
    for line in infile:
        if line.startswith('#'): continue
        word = line.split()[1].decode('utf-8')
        if len(word) > 1: words.add(word)
    infile.close()
    outfile = open(sys.argv[2], 'w')
    for word in list(words): outfile.write((u'%s 1\n' % word).encode('utf-8'))
    outfile.close()
