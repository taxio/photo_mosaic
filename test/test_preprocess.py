from unittest import TestCase
from nose.tools import eq_
import sqlite3

from PIL import Image
from photo_mosaic import ImportImages


class TestPreprocess(TestCase):

    def setUp(self):
        self.import_image = ImportImages(dbname='./test/test.sqlite3', img_dir_path='./test/img')

    def tearDown(self):
        self.import_image.drop_table()

    def test_calc_mean(self):
        # データベース更新
        self.import_image.calc_mean()

        conn = sqlite3.connect('./test/test.sqlite3')
        c = conn.cursor()
        c.execute('select * from materials')
        materials = c.fetchall()
        eq_(6, len(materials))
