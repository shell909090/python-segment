# 简介 #

cls是分类系统，负责各种分类器的console界面。

# 参数 #

* -d: 用于指定分词词典。
* -f: 用于指定统计频率词典。

# 命令 #

* create_fisher: 从一个txt词库生成一个fisher的marshal词库，如果目标词库存在则覆盖原始内容。

	ps_cls create_fisher

	注意，内容为空。

* train_fisher: 统计ham目录和spam目录，并且更新数据库。

	ps_cls train_fisher hamdir spamdir

* classify_fisher: 分析文件，计算出归属ham和spam的可能性。

	ps_cls classify_fisher spam.txt
