#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2010-10-01
@author: shell.xu
'''
import unittest
import segment

from pathlib import Path

db = segment.dictdb()
db.importtxt(Path(__file__).with_name('dict.txt.gz'))

class utCutter(unittest.TestCase):

    def setUp(self):
        self.c = segment.StringCutter(None)

    def test_english_words(self):
        self.assertEqual(list(self.c.parse("BigBigPig")),
                         ["Big","Big","Pig"])

    def test_not_english_words(self):
        self.assertEqual(list(self.c.parse("LOLI")),
                         ["LOLI"])

    def test_english_number(self):
        self.assertEqual(list(self.c.parse("abc123")),
                         ["abc", "123"])

    def test_chinese_number(self):
        self.assertEqual(list(self.c.parse("我们123")),
                         ["我们", "123"])

    def test_chinese_english(self):
        self.assertEqual(list(self.c.parse("我们abc")),
                         ["我们", "abc"])

    def test_mix(self):
        self.assertEqual(list(self.c.parse("我们123abc")),
                         ["我们", "123", "abc"])

    def test_number(self):
        self.assertEqual(list(self.c.parse("abc123,456")),
                         ["abc","123,456"])

    def test_split(self):
        self.assertEqual(list(self.c.parse("abc,def")),
                         ["abc", ",", 'def'])
        self.assertEqual(list(self.c.parse("xyz：ddd")),
                         ["xyz", "：", 'ddd'])

    def test_english_punct(self):
        self.assertEqual(list(self.c.parse("we're half-ready")),
                         ["we're", " ", "half-ready"])

    def test_not_number(self):
        rslt = ["we", "‘", "re", " ", "half", "——", "ready"]
        self.assertEqual(list(self.c.parse("we‘re half——ready")), rslt)

class utDynamic(unittest.TestCase):
    def setUp(self):
        self.c = segment.DynamicCutter(db)

    def test1(self):
        self.assertEqual(list(self.c.parse('有机会见面')),
                         ['有', '机会', '见面'])

    def test2(self):
        self.assertEqual(list(self.c.parse('长春市长春节致辞')),
                         ['长春', '市长', '春节', '致辞'])
        
    def test3(self):
        self.assertEqual(list(self.c.parse('长春市长春药店')),
                         ['长春市', '长春', '药店'])

    def test4(self):
        self.assertEqual(list(self.c.parse('有意见分歧')),
                         ['有', '意见分歧'])

    def test5(self):
        rslt = ['吹毛求疵', '和鱼鹰是', '两个',
                '有', '魔力', '的', '单词']
        self.assertEqual(list(self.c.parse('吹毛求疵和鱼鹰是两个有魔力的单词')), rslt)

    def test6(self):
        self.assertEqual(list(self.c.parse('王强大小')),
                         ['王', '强大', '小'])

    def test7(self):
        self.assertEqual(list(self.c.parse('毛泽东北京华烟云')),
                         ['毛泽东', '北京', '华', '烟云'])

    def test8(self):
        self.assertEqual(list(self.c.parse('魔王育成计划')),
                         ['魔王', '育成', '计划'])

    def test9(self):
        self.assertEqual(list(self.c.parse('遥远古古巴比伦')),
                         ['遥远', '古', '古', '巴比伦'])

if __name__ == '__main__': unittest.main()
