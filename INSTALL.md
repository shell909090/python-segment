# 准备 #

如果你不准备进行安装部署，可以跳过安装和打包这两步。如果你打算使用cutter工具，请安装chardet。如果你打算使用spider工具，请安装html2text。

# 获得代码 #

你可以使用以下代码，直接从版本库中复制一个可用版本出来。

	hg clone https://shell909090@code.google.com/p/python-segment/

或者可以从这里下载一个最新版本的包。

# 直接安装 #

使用setup.py直接安装。

# debian打包 #

debuild直接打包。

# 词典生成 #

按照如下方式，使用dbmgr生成frq.db文件。

	gunzip dict.tar.gz
	./ps_dbmgr create dict.txt

你可以看到生成了frq.db，这是词典的默认文件名。注意，词典文件的格式和具体的版本有关，换用版本后最好重新生成词典。

# 命令行使用 #

假定有一个文本文件，test.txt，里面内容是中文平文本，编码任意。

	./ps_cutter cutshow test.txt

cutter会自动推测编码。

# 代码使用 #

假如当前有一个frq.db词库。

	import segment
	cut = segment.get_cutter('frq.db')
	print list(cut.parse(u'工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作'))

注意，仅仅使用parse是不会进行分词的，因为parse返回的是一个生成器。

# 分类器命令行例子 #

假定有一个spam目录，一个ham目录，一个example.txt文件。以下过程可以分析example.txt归属于哪个分类。

	./ps_cls create_fisher
	./ps_cls train_fisher hamdir/ spam/
	./ps_cls classify_fisher example.txt
