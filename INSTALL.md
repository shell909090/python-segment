# 安装与运行

需要 Python 3.11 或更高版本和 uv。

```sh
uv sync
# 如需网页采集训练工具 ps_spider：
uv sync --extra spider
```

运行爬虫时使用 `uv run --extra spider ps_spider ...`，确保可选依赖已安装。

# 词典生成

可直接导入项目附带的 gzip 词典，无需解压：

```sh
uv run ps_dbmgr create dict.txt.gz
uv run ps_dbmgr stat
uv run ps_cutter cutstr '我爱北京天安门'
uv run ps_cutter cutshow test.txt
uv run python example.py
```

默认词典为当前目录的 `frq.db`；可通过 `-d` 指定路径。
旧 Python 2 的 marshal 数据库请从文本词典重新生成。

# 代码使用

```python
import segment

cut = segment.get_cutter('frq.db')
print(list(cut.parse('我爱北京天安门')))
```

`parse()` 返回生成器，迭代后才执行分词或训练。

# 分类器

```sh
uv run ps_cls create_fisher
uv run ps_cls train_fisher ham/ spam/
uv run ps_cls classify_fisher example.txt
```

# 检查和构建

```sh
uv run python -m unittest discover -v
uv build
```

测试直接读取附带词典，不依赖工作目录中已生成的数据库。
Debian 打包使用 Python 3、dh-python 和 pybuild，需要先安装 debian/control 中的构建依赖。
