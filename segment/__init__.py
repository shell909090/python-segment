#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
from dbase import readfile_cd
from dictdb import dictdb
from cut import StringCutter
from dyn import DynamicCutter
from train import StatCutter, NewCutter
from fisher import Fisher

def get_cutter(filepath):
    return StringCutter(DynamicCutter(dictdb(filepath)))
