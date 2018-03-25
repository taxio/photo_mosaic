from unittest import TestCase
from nose.tools import eq_, ok_
import sqlite3

from PIL import Image
from photo_mosaic import ImportImages
import photo_mosaic.util


class TestPreprocess(TestCase):

    def setUp(self):
        self.import_image = ImportImages(dbname='./test/test.sqlite3')

    def tearDown(self):
        self.import_image.drop_table()

    def test_calc_mean(self):
        # データベース更新
        img_names = photo_mosaic.util.get_image_names('./test/img')
        for img_name in img_names:
            mat = self.import_image.calc_mean(img_name)
            if mat.name == './test/img/yellow.png':
                ok_(abs(mat.R - 253.885572139303) < 0.000000001)
                ok_(abs(mat.G - 224.129353233831) < 0.000000001)
                ok_(abs(mat.B - 10.0199004975124) < 0.000000001)

    def test_calc_all(self):
        self.import_image.calc_all('./test/img')
        conn = sqlite3.connect('./test/test.sqlite3')
        c = conn.cursor()
        c.execute('select * from materials')
        mats = c.fetchall()
        eq_(7, len(mats))
        conn.close()

    def test_insert_image(self):
        conn = sqlite3.connect('./test/test.sqlite3')
        c = conn.cursor()
        c.execute('select * from materials')
        mats = c.fetchall()
        tmp = len(mats)
        self.import_image.insert_image('./test/img/yellow.png')
        c.execute('select * from materials')
        mats = c.fetchall()
        eq_(tmp+1, len(mats))
        conn.close()

