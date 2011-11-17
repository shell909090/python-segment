#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-10-02
@author: shell.xu
'''
from distutils.core import setup

setup(name = 'segment', version = '1.0', url = 'http://shell909090.com/',
      author = 'Shell.E.Xu', author_email = 'shell909090@gmail.com',
      description = 'segmentation library written by python',
      packages = ['segment',], scripts=['ps_cutter', 'ps_dbmgr'])
