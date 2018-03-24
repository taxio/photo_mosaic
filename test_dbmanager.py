from unittest import TestCase
from nose.tools import eq_
import sqlite3

from photo_mosaic import dbmanager

class TestDBManager(TestCase):

    def setUp(self):
        self._db = dbmanager.DBManager('./test/test.sqlite3', debug=False)

    def tearDown(self):
        self._db.drop_table()

    def test_insert_and_get(self):
        mat = dbmanager.MaterialImage(
                name='test_image',
                R = 123.456,
                G = 111.22222,
                B = 333.123456
                )
        self._db.insert_material(mat)

        mats = self._db.get_materials()
        eq_(1, len(mats))
        eq_('test_image', mats[0].name)
        eq_(123.456, mats[0].R)
        eq_(111.22222, mats[0].G)
        eq_(333.123456, mats[0].B)

