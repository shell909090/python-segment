# 简介 #

dbmgr是词典管理工具，他提供了词典的console管理界面。

# 参数 #

* -d: 用于指定目标marshal词典。

# 命令 #

* create: 从一个txt词库生成一个marshal词库，如果目标词库存在则覆盖原始内容。

	ps_dbmgr create dict.txt

	dict.txt必须存在且格式正确，文件编码必须为utf-8，且格式正确。

* importdb: 从一个txt词库导入数据，目标词库必须存在，新数据叠加到目标词库上。

	ps_dbmgr importdb dict.txt

* exportdb: 导出数据到txt文件上，目标如果存在则覆盖。

	ps_dbmgr exportdb dict.txt

* add: 增加中文词语词频。如果词语不存在则添加。

	ps_dbmgr add 中文 10

* remove: 删除中文词语。

	ps_dbmgr remove 中文

* lookup: 查找中文字和词语的对数频率。

	ps_dbmgr lookup 中文

	注意，长度为1的会查找字频表，而长度超过1会查找词频表。表中不存在的字词会按照出现概率为1进行计算。

* cals: 计算该字符串的对数频率和。不理会其中的词语，直接将字符串中的每个字的对数频率求和。

	ps_dbmgr cals 中文

* stat: 词语数据库的统计数据。包括有多少个词，总词频多少，平均词频多少，最高词频多少，首层dict宽度，平均二层宽度。

	ps_dbmgr stat

* waterlevel: 计算该水位以上的词语数量。即查找出现次数大于等于当前值的所有词语总量。

	ps_dbmgr waterlevel 1.1

* scale: 所有词语的出现次数乘以一个调整因子。

	ps_dbmgr scale 0.9

	该功能通常用于词库合并，将两个词库的平均出现频率调整到一致后进行合并比较好。

* shrink: 切割词库，删除所有小于指定水平的词。

	ps_dbmgr shrink 0.9

	可以通过waterlevel计算出还会残留多少词。

* flat: 扁平化，将所有词频调整为1。

	ps_dbmgr flat

* trans_cedict: 将cedict词典转换为可用的txt词典。

	ps_dbmgr trans_cedict in.txt out.txt

* trans_plain: 将无词频平文本词典转换为可用的txt词典。

	ps_dbmgr trans_plain in.txt out.txt
