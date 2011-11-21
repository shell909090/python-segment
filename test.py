#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-10-01
@author: shell.xu
'''
import unittest
import segment

db = segment.dictdb('frq.db')

class utCutter(unittest.TestCase):

    def setUp(self):
        self.c = segment.StringCutter(None)

    def test_english_words(self):
        self.assertEqual(list(self.c.parse(u"BigBigPig")),
                         [u"Big",u"Big",u"Pig"])

    def test_not_english_words(self):
        self.assertEqual(list(self.c.parse(u"LOLI")),
                         [u"LOLI"])

    def test_english_number(self):
        self.assertEqual(list(self.c.parse(u"abc123")),
                         [u"abc", u"123"])

    def test_chinese_number(self):
        self.assertEqual(list(self.c.parse(u"我们123")),
                         [u"我们", u"123"])

    def test_chinese_english(self):
        self.assertEqual(list(self.c.parse(u"我们abc")),
                         [u"我们", u"abc"])

    def test_mix(self):
        self.assertEqual(list(self.c.parse(u"我们123abc")),
                         [u"我们", u"123", u"abc"])

    def test_number(self):
        self.assertEqual(list(self.c.parse(u"abc123,456")),
                         [u"abc",u"123,456"])

    def test_split(self):
        self.assertEqual(list(self.c.parse(u"abc,def")),
                         [u"abc", u",", u'def'])
        self.assertEqual(list(self.c.parse(u"xyz：ddd")),
                         [u"xyz", u"：", u'ddd'])

    def test_english_punct(self):
        self.assertEqual(list(self.c.parse(u"we're half-ready")),
                         [u"we're", u" ", u"half-ready"])

    def test_not_number(self):
        rslt = [u"we", u"‘", u"re", u" ", u"half", u"——", u"ready"]
        self.assertEqual(list(self.c.parse(u"we‘re half——ready")), rslt)

class utDynamic(unittest.TestCase):
    def setUp(self):
        self.c = segment.DynamicCutter(db, None)

    def test1(self):
        self.assertEqual(list(self.c.parse(u'有机会见面')),
                         [u'有', u'机会', u'见面'])

    def test2(self):
        self.assertEqual(list(self.c.parse(u'长春市长春节致辞')),
                         [u'长春', u'市长', u'春节', u'致辞'])
        
    def test3(self):
        self.assertEqual(list(self.c.parse(u'长春市长春药店')),
                         [u'长春市', u'长春', u'药店'])

    def test4(self):
        self.assertEqual(list(self.c.parse(u'有意见分歧')),
                         [u'有', u'意见分歧'])

    def test5(self):
        rslt = [u'吹毛求疵', u'和鱼鹰是', u'两个',
                u'有', u'魔力', u'的', u'单词']
        self.assertEqual(list(self.c.parse(u'吹毛求疵和鱼鹰是两个有魔力的单词')), rslt)

    def test6(self):
        self.assertEqual(list(self.c.parse(u'王强大小')),
                         [u'王', u'强大', u'小'])

    def test7(self):
        self.assertEqual(list(self.c.parse(u'毛泽东北京华烟云')),
                         [u'毛泽东', u'北京', u'华', u'烟云'])

    def test8(self):
        self.assertEqual(list(self.c.parse(u'魔王育成计划')),
                         [u'魔王', u'育成', u'计划'])

    def test9(self):
        self.assertEqual(list(self.c.parse(u'遥远古古巴比伦')),
                         [u'遥远', u'古', u'古', u'巴比伦'])

if __name__ == '__main__': unittest.main()
