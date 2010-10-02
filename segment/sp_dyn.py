#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-10-01
@author: shell.xu
'''
from word_dict import word_dict

def cmp_subtree(rslt1, rslt2):
    if rslt1 is None: return True
    c1 = sum([len(r) for r, i in rslt1 if i == 0])
    c2 = sum([len(r) for r, i in rslt2 if i == 0])
    if c1 > c2: return True
    elif c1 < c2: return False
    c1 = len([r for r, i in rslt1 if i != 0])
    c2 = len([r for r, i in rslt2 if i != 0])
    if c1 > c2: return True
    elif c1 < c2: return False
    c1 = sum([r[1] for r in rslt1])
    c2 = sum([r[1] for r in rslt2])
    return c1 < c2

cache = {}
def memoiza(fun):
    def proc(*arg):
        if arg in cache: return cache[arg]
        x = fun(*arg)
        cache[arg] = x
        return x
    return proc

def find_first_match(sentence, start_pos = 0):
    for i in xrange(start_pos, len(sentence)):
        cutterset = word_dict.match(sentence[i:])
        if cutterset: return i, cutterset
    return 0, []

def dyn_split(sentence):
    if not sentence: return []
    if len(sentence) < 2: return [(sentence, 0),]
    best_rslt = None
    poc, cutterset = find_first_match(sentence)
    if poc == 0: pre_cut = None
    else: pre_cut, sentence = sentence[:poc], sentence[poc:]
    if not cutterset: minlen = len(sentence)
    else: minlen = min([len(c[0]) for c in cutterset])
    poc, c = find_first_match(sentence, 1)
    while poc < minlen and c:
        temp_rslt = [(sentence[:poc], 0),] + dyn_split(sentence[poc:])
        if cmp_subtree(best_rslt, temp_rslt): best_rslt = temp_rslt
        poc, c = find_first_match(sentence, poc + 1)
    for cutter, frq in cutterset:
        temp_rslt = [(cutter, frq),] + dyn_split(sentence[len(cutter):])
        if cmp_subtree(best_rslt, temp_rslt): best_rslt = temp_rslt
    if best_rslt is None: best_rslt = [(sentence, 0),]
    if pre_cut: best_rslt.insert(0, (pre_cut, 0))
    # print '%s => %s' % (sentence, best_rslt)
    return best_rslt

class DynamicSpliter(object):
    def __init__(self, next): self.next, self.cache = next, {}
    def parse(self, word, **kargs):
        if kargs.get('break_char', False):
            self.next.parse(word, **kargs)
            self.cache = {}
        if kargs.get('passwd', False): self.next.parse(word, **kargs)
        for word, frq in dyn_split(word):
            if frq == 0: self.next.parse(word)
            else: self.next.parse(word, passwd = True, frq = frq)
    def parse_array(self, a): map(self.parse, a)
