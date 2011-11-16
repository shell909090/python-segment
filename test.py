#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-10-01
@author: shell.xu
'''
import unittest
from segment import word_dict, ContAll, CutterSpliter, DynamicSpliter

class utCutter(unittest.TestCase):
    def setUp(self):
        self.p = ContAll()
        self.c = CutterSpliter(self.p)
    def test_english_words(self):
        self.c.parse_array([u"BigBigPig"])
        self.assertEqual(self.p.get_result(), [u"Big",u"Big",u"Pig"])
    def test_not_english_words(self):
        self.c.parse_array([u"LOLI"])
        self.assertEqual(self.p.get_result(), [u"LOLI"])
    def test_english_number(self):
        self.c.parse_array([u"abc123"])
        self.assertEqual(self.p.get_result(), [u"abc",u"123"])
    def test_chinese_number(self):
        self.c.parse_array([u"我们123"])
        self.assertEqual(self.p.get_result(), [u"我们",u"123"])
    def test_chinese_english(self):
        self.c.parse_array([u"我们abc"])
        self.assertEqual(self.p.get_result(), [u"我们",u"abc"])
    def test_mix(self):
        self.c.parse_array([u"我们123abc"])
        self.assertEqual(self.p.get_result(), [u"我们",u"123",u"abc"])
    def test_number(self):
        self.c.parse_array([u"abc123,456"])
        self.assertEqual(self.p.get_result(), [u"abc",u"123,456"])
    def test_split(self):
        self.c.parse_array([u"abc,def", u"xyz：ddd"])
        self.assertEqual(self.p.get_result(), [u"abc",u',',u"def",u"xyz",u'：',u"ddd",])
    def test_english_punct(self):
        self.c.parse_array([u"we're half-ready"])
        self.assertEqual(self.p.get_result(), [u"we're", u" ", u"half-ready"])
    def test_not_number(self):
        self.c.parse_array([u"we‘re half——ready"])
        self.assertEqual(self.p.get_result(), [u"we", u"‘", u"re", u" ", u"half", u"——", u"ready"])

class utDynamic(unittest.TestCase):
    def setUp(self):
        self.p = ContAll()
        self.c = DynamicSpliter(self.p)
    def test1(self):
        self.c.parse(u'有机会见面')
        self.assertEqual(self.p.get_result(), [u'有', u'机会', u'见面'])
    def test2(self):
        self.c.parse(u'长春市长春节致辞')
        self.assertEqual(self.p.get_result(), [u'长春', u'市长', u'春节', u'致辞'])
    def test3(self):
        self.c.parse(u'长春市长春药店')
        self.assertEqual(self.p.get_result(), [u'长春市', u'长春', u'药店'])
    def test4(self):
        self.c.parse(u'有意见分歧')
        self.assertEqual(self.p.get_result(), [u'有', u'意见', u'分歧'])
    def test5(self):
        self.c.parse(u'吹毛求疵和鱼鹰是两个有魔力的单词')
        self.assertEqual(self.p.get_result(), [u'吹毛求疵', u'和', u'鱼鹰', u'是两个有', u'魔力', u'的', u'单词'])
    def test6(self):
        self.c.parse(u'王强大小')
        self.assertEqual(self.p.get_result(), [u'王', u'强', u'大小'])
    def test7(self):
        self.c.parse(u'毛泽东北京华烟云')
        self.assertEqual(self.p.get_result(), [u'毛泽东', u'北京', u'华烟云'])
    def test8(self):
        self.c.parse(u'魔王育成计划')
        self.assertEqual(self.p.get_result(), [u'魔王', u'育成', u'计划'])
    def test9(self):
        self.c.parse(u'遥远古古巴比伦')
        self.assertEqual(self.p.get_result(), [u'遥', u'远古', u'古巴比伦'])

def cuttest(word):
    p = ContAll()
    c = DynamicSpliter(p)
    c.parse(word.decode('utf-8'))
    print u', '.join([u'u\'%s\'' % i for i in p.get_result()])

def test_dyn1():
    # cuttest("这是一个伸手不见五指的黑夜。我叫孙悟空，我爱北京，我爱Python和C++。")
    # cuttest("我不喜欢日本和服。")
    # cuttest("雷猴回归人间。")
    # cuttest("工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作")
    # cuttest("我需要廉租房")
    # cuttest("永和服装饰品有限公司")
    # cuttest("我爱北京天安门")
    # cuttest("abc")
    # cuttest("隐马尔可夫")
    # cuttest("雷猴是个好网站")
    # cuttest("“Microsoft”一词由“MICROcomputer（微型计算机）”和“SOFTware（软件）”两部分组成")
    # cuttest("草泥马和欺实马是今年的流行词汇")
    # cuttest("伊藤洋华堂总府店")
    # cuttest("中国科学院计算技术研究所")
    # cuttest("罗密欧与朱丽叶")
    # cuttest("我购买了道具和服装")
    # cuttest("PS: 我觉得开源有一个好处，就是能够敦促自己不断改进，避免敞帚自珍")
    # cuttest("湖北省石首市")
    # cuttest("总经理完成了这件事情")
    # cuttest("电脑修好了")
    # cuttest("做好了这件事情就一了百了了")
    # cuttest("人们审美的观点是不同的")
    # cuttest("我们买了一个美的空调")
    # cuttest("线程初始化时我们要注意")
    # cuttest("一个分子是由好多原子组织成的")
    pass

def test_dyn2():
    # cuttest("祝你马到功成")
    # cuttest("他掉进了无底洞里")
    # cuttest("中国的首都是北京")
    # cuttest("孙君意")
    # cuttest("外交部发言人马朝旭")
    # cuttest("领导人会议和第四届东亚峰会")
    # cuttest("在过去的这五年")
    # cuttest("还需要很长的路要走")
    # cuttest("60周年首都阅兵")
    # cuttest("你好人们审美的观点是不同的")
    # cuttest("买水果然后来世博园")
    # cuttest("买水果然后去世博园")
    # cuttest("但是后来我才知道你是对的")
    # cuttest("存在即合理")
    # cuttest("的的的的的在的的的的就以和和和")
    # cuttest("I love你，不以为耻，反以为rong")
    # cuttest("hello你好人们审美的观点是不同的")
    # cuttest("很好但主要是基于网页形式")
    # cuttest("hello你好人们审美的观点是不同的")
    # cuttest("为什么我不能拥有想要的生活")
    # cuttest("后来我才")
    # cuttest("此次来中国是为了")
    # cuttest("使用了它就可以解决一些问题")
    # cuttest(",使用了它就可以解决一些问题")
    # cuttest("其实使用了它就可以解决一些问题")
    # cuttest("好人使用了它就可以解决一些问题")
    # cuttest("是因为和国家")
    # cuttest("老年搜索还支持")
    # cuttest("干脆就把那部蒙人的闲法给废了拉倒！RT @laoshipukong : 27日，全国人大常委会第三次审议侵权责任法草案，删除了有关医疗损害责任“举证倒置”的规定。在医患纠纷中本已处于弱势地位的消费者由此将陷入万劫不复的境地。 ")
    pass

if __name__ == '__main__':
    # word_dict.load_text('cedict.txt')
    word_dict.load_pick('cedict.pick')
    unittest.main()
