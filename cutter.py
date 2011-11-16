#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
import os, sys, time
import segment

cut = segment.get_cutter('frq.db')

def main():
    with open(sys.argv[1], 'r') as fi: data = fi.read().decode('gbk')
    # print data
    # print '|'.join(cut.parse(data))
    list(cut.parse(data))

if __name__ == '__main__': main()
