# 简介 #

python-segment是一个纯python实现的分词库，他的目标是提供一个可用的，完善的分词系统和训练环境，包括一个可用的词典。

# 词典说明 #

python-segment的词典是带词频无词性词典，程序基于剪枝和词频概率工作，不考虑词性，不考虑马尔可夫链。词典含两部分内容，单字词频和词组词频。两者的统计和使用是分离的。

* 单字词频，某个词的出现次数。
* 词粗词频，某个词组的出现次数。 

词典一般有两种形态，marshal格式和txt格式，dbmgr工具提供了词典的管理界面。

# 词频规则 #

词频有两种表示方法，一种为词语的出现次数。在marshal词典和txt词典中使用此种表示方法。另一种为词的出现次数除以总词量的对数，在计算中通常采用后者。在实际计算概率的时候，采用通乘所有碎片的概率。使用对数词频可以将这一行为化为加法。

# 内置词典使用说明 #

内置词典是txt格式词典，通过gzip压缩。解压后使用dbmgr可以生成一个marshal格式词典。

# 性能说明 #

在一台虚拟机上测试的结果，载入词典后消耗内存（带python）大约60m，分词效率大约100k字/秒。注意，默认情况下，程序使用yield返回分词结果，这不会消耗太多内存。但是如果需要保留分词得到的每个词语碎片，将耗费大量内存。根据测试，一个10M的文本文件（大约500W字）需要120m以上的内存来保持词语碎片。 

# 授权 #

The MIT License (MIT)

Copyright (c) 2010 Shell.Xu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
