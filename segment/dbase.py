#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-24
@author: shell.xu
'''
class dbase(object):

    def __init__(self, filepath = None):
        self.close()
        self.filepath = filepath
        if self.filepath: self.loadfile(filepath)

    def sync(self):
        if self.filepath: self.savefile(self.filepath)

    def savefile(self, filepath):
        with open(filepath, 'w') as fo: self.save(fo)
    def loadfile(self, filepath):
        with open(filepath, 'r') as fi: self.load(fi)
