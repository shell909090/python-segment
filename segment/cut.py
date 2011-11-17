#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2011-11-16
@author: shell.xu
'''
import unicodedata
chrcat = unicodedata.category

punct_set = set(['Ll', 'Lu', 'Lo', 'Nd'])
def split_punct(stc, s):
    for e in xrange(s, len(stc)):
        if chrcat(stc[e]) in punct_set: return e
    return len(stc)

def split_chinese(stc, s):
    for e in xrange(s, len(stc)):
        if chrcat(stc[e]) != 'Lo': return e
    return len(stc)

def split_english(stc, s):
    for e in xrange(s, len(stc)):
        t = chrcat(stc[e])
        if t not in ['Lu', 'Ll'] and stc[e] not in '-.\'': return e
        if e != s and pre_type == 'Ll' and t == 'Lu': return e
        pre_type = t
    return len(stc)

def split_number(stc, s):
    for e in xrange(s, len(stc)):
        t = chrcat(stc[e])
        if t != 'Nd' and stc[e] not in u',.': return e
    return len(stc)

class StringCutter(object):
    def __init__(self, next): self.next = next

    def parse(self, stc):
        s, l = 0, len(stc)
        while s < l:
            t = chrcat(stc[s])
            if t == 'Lo':
                e = split_chinese(stc, s)
                if not self.next: yield stc[s:e]
                else:
                    for i in self.next.parse(stc[s:e]): yield i
            elif t == 'Nd':
                e = split_number(stc, s)
                if self.next: self.next.stop()
                yield stc[s:e]
            elif t in ['Ll', 'Lu']:
                e = split_english(stc, s)
                if self.next: self.next.stop()
                yield stc[s:e]
            else:
                e = split_punct(stc, s)
                if self.next: self.next.stop()
                yield stc[s:e]
            s = e
