"""Python 3 dictionary, training and command-line regression tests."""
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import segment

ROOT = Path(__file__).resolve().parent


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.dbpath = self.base / 'frq.db'
        self.db = segment.dictdb()
        self.db.importtxt(ROOT / 'dict.txt.gz')
        self.db.savefile(self.dbpath)

    def cli(self, script, *args):
        result = subprocess.run(
            [sys.executable, str(ROOT / script), *map(str, args)],
            cwd=self.base, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        return result.stdout

    def test_dictionary_roundtrip(self):
        out = io.StringIO()
        self.db.exporttxt(out)
        source = self.base / 'dict.txt'
        source.write_text(out.getvalue(), encoding='utf-8')
        other = segment.dictdb()
        other.importtxt(source)
        self.assertEqual(other.db, self.db.db)
        self.assertEqual(other.sdb, self.db.sdb)
        self.assertEqual(segment.dictdb(self.dbpath).db, self.db.db)

    def test_text_and_cli(self):
        source = self.base / 'input.txt'
        text = '我爱北京天安门。' * 30
        source.write_bytes(text.encode('gb18030'))
        self.assertEqual(segment.readfile_cd(source), text)
        self.assertIn('北京', self.cli('ps_cutter', 'cutshow', source))
        self.assertIn('北京', self.cli('ps_cutter', 'cutstr', '我爱北京天安门'))
        self.cli('ps_dbmgr', 'waterlevel', '10')
        self.cli('ps_dbmgr', 'exportdb', self.base / 'export.txt')

    def test_frequency_training_persists(self):
        source = self.base / 'input.txt'
        source.write_text('北京北京', encoding='utf-8')
        before = dict(self.db.items())['北京']
        self.cli('ps_cutter', 'frqtrain', source)
        after = dict(segment.dictdb(self.dbpath).items())['北京']
        self.assertEqual(after, before + 2)
        folder = self.base / 'corpus'
        folder.mkdir()
        (folder / 'input.txt').write_text('北京北京', encoding='utf-8')
        self.cli('ps_cutter', 'frqtrains', folder)
        self.assertEqual(dict(segment.dictdb(self.dbpath).items())['北京'], before + 4)

    def test_new_word_training(self):
        new = segment.NewCutter(self.db)
        self.assertEqual(new.get_highfrq(), [])
        list(new.parse('龘靐齉'))
        self.assertEqual(new.wordfrq['龘靐齉'], 1)
        source = self.base / 'input.txt'
        source.write_text('龘靐齉', encoding='utf-8')
        self.cli('ps_cutter', 'newtrain', source)

    def test_dictionary_conversion(self):
        source = self.base / 'plain.txt'
        source.write_text('北京\n上海\n', encoding='utf-8')
        target = self.base / 'converted.txt'
        self.cli('ps_dbmgr', 'trans_plain', source, target)
        self.assertEqual(set(target.read_text().splitlines()), {'北京 1', '上海 1'})
        source.write_text('北京 北京 [bei3 jing1] /Beijing/\n', encoding='utf-8')
        self.cli('ps_dbmgr', 'trans_cedict', source, target)
        self.assertEqual(target.read_text(), '北京 1\n')

    def test_classifier(self):
        for category, text in [('ham', '北京天气很好'), ('spam', '购买商品优惠')]:
            folder = self.base / category
            folder.mkdir()
            (folder / 'input.txt').write_text(text, encoding='utf-8')
        self.cli('ps_cls', 'create_fisher')
        self.cli('ps_cls', 'train_fisher', self.base / 'ham', self.base / 'spam')
        out = self.cli('ps_cls', 'classify_fisher', self.base / 'ham/input.txt')
        self.assertIn('ham', out)
        self.assertIn('spam', out)
