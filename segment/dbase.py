#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-24
@author: shell.xu
'''
import chardet

class dbase(object):
    def __init__(self, filepath = None):
        self.close()
        self.filepath = filepath
        if self.filepath: self.loadfile(filepath)

    def sync(self):
        if self.filepath: self.savefile(self.filepath)

    def savefile(self, filepath):
        with open(filepath, 'wb') as fo: self.save(fo)
    def loadfile(self, filepath):
        with open(filepath, 'rb') as fi: self.load(fi)

def readfile_cd(filepath):
    with open(filepath, 'r') as fi: data = fi.read()
    if len(data) < 120: enc = chardet.detect(data)['encoding']
    else: enc = chardet.detect(data[:120])['encoding']
    if enc is None: enc = 'utf-8'
    return data.decode(enc, 'ignore')

class CutterBase(object):
    def parsefile(self, filepath):
        print 'process', filepath
        return self.parse(readfile_cd(filepath))

