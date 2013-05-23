# 简介 #

cutter是分词和训练的console界面。

# 参数 #

* -d: 用于指定目标marshal词典。

# 命令 #

* cutstr: cutstr将一个句子分词，并且在屏幕上展现分词过程。

	cutstr: cutstr sentence : cut string and show out.

* cut: cut负责分词一个或多个文件，不在屏幕上打印。

	cut: cut filepath ... : cut a file and not print out.

* cutshow: cutshow负责分词一个或多个文件，在屏幕上打印。

	cutshow: cutshow filepath ... : cut a file and print out.

* frqtrain: frqtrain负责训练一个或多个文件的词频。

	frqtrain: frqtrain filepath ... : train frequency by files.

* frqtrains: frqtrains负责训练一个目录下所有文件的词频。

	frqtrains: frqtrains dirpath : train frequency by all files under dir.

* newtrain: newtrain负责训练一个或多个文件的新词。

	newtrain: newtrain filepath ... : train new words by files.

* newtrains: newtrains负责训练一个目录下所有文件的新词。

	newtrains: newtrains dirpath : train new words by all files under dir.

* frqstat: frqstat负责训练一个或多个文件的字频。

	frqstat: frqstat filepath ... : statistics frequency of char in files.

* frqstats: frqstats负责训练一个目录下所有文件的字频。

	frqstats: frqstats dirpath : statistics frequency in all files under dir.
