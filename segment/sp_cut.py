#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-10-01
@author: shell.xu
'''
import unicodedata
char_category = unicodedata.category

def split_punct(s, startpos):
    l = len(s)
    for e in xrange(startpos, l):
        if char_category(s[e]) in ['Ll', 'Lu', 'Lo', 'Nd']: return e
    return l

def split_chinese(s, startpos):
    l = len(s)
    for e in xrange(startpos, l):
        if char_category(s[e]) != 'Lo': return e
    return l

def split_english(s, startpos):
    l = len(s)
    for e in xrange(startpos, l):
        t = char_category(s[e])
        if t not in ['Lu', 'Ll'] and s[e] not in '-.\'': return e
        if e != startpos and pre_type == 'Ll' and t == 'Lu': return e
        pre_type = t
    return l

def split_number(s, startpos):
    l = len(s)
    for e in xrange(startpos, l):
        t = char_category(s[e])
        if t != 'Nd' and s[e] not in u',.': return e
    return l

def split_string(s, startpos):
    t = char_category(s[startpos])
    if t == 'Lo':
        e = split_chinese(s, startpos)
        return 0, s[startpos:e], e
    elif t == 'Nd':
        e = split_number(s, startpos)
        return 2, s[startpos:e], e
    elif t in ['Ll', 'Lu']:
        e = split_english(s, startpos)
        return 1, s[startpos:e], e
    else:
        e = split_punct(s, startpos)
        return 3, s[startpos:e], e

class CutterSpliter(object):
    def __init__(self, next): self.next = next
    def parse(self, word, **kargs):
        s, l = 0, len(word)
        while s < l:
            t, p, s = split_string(word, s)
            if t == 3: self.next.parse(p, passed = True, break_char = True, **kargs)
            elif t == 2 or t == 1: self.next.parse(p, passed = True, **kargs)
            else: self.next.parse (p, **kargs)
    def parse_array(self, a): map(self.parse, a)

class ContPrint(object):
    def parse(self, word, **kargs):
        print word

class ContAll(object):
    def __init__(self): self.rslt = []
    def parse(self, word, **kargs):
        if word: self.rslt.append(word)
    def get_result(self): return self.rslt
