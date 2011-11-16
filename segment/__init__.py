#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
from dictdb import dictdb
from cut import StringCutter
from dyn import DynamicCutter

def get_cutter(filepath):
    db = dictdb()
    db.loadfile(filepath)
    return StringCutter(DynamicCutter(db, None))
