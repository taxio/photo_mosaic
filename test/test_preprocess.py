from unittest import TestCase
from nose.tools import eq_

from PIL import Image
from photo_mosaic import ImportImages


class TestPreprocess(TestCase):

    def setUp(self):
        self.import_image = ImportImages(dbname='./test/test.sqlite3', img_dir_path='./test/img')

    def tearDown(self):
        self.import_image.drop_table()

    def test_calc_mean(self):
        pass


