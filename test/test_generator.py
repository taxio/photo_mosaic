from unittest import TestCase
from nose.tools import eq_

from photo_mosaic import PhotoMosaicGenerator, PreProcess 

class TestGenerator(TestCase):

    def setUp(self):
        self.pre = PreProcess('./test/test.sqlite3')

    def tearDown(self):
        self.pre.drop_table()

    def test_generate(self):
        self.pre.calc_all('./test')
        
        generator = PhotoMosaicGenerator(materials_db='./test/test.sqlite3')
        eq_('./test/img/red.png', generator.get_near_image_name((255, 0, 0), 0))
        eq_('./test/img/green.png', generator.get_near_image_name((0, 255, 0), 0))
        eq_('./test/img/blue.png', generator.get_near_image_name((0, 0, 255), 0))

        generator.generate(
                target_image_name='./test/img/target.png', 
                output_image_name='./test/img/output.png', 
                n_split=2)


