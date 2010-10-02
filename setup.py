#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-10-02
@author: shell.xu
'''
from distutils.core import setup

py_modules = ['segment.sp_cut', 'segment.sp_dyn', 'segment.word_dict',]

setup(name = 'segment', version = '1.0', url = 'http://shell909090.com/',
      author = 'Shell.E.Xu', author_email = 'shell909090@gmail.com',
      py_modules = py_modules)
