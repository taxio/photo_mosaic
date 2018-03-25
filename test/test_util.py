from unittest import TestCase
from nose.tools import eq_

from PIL import Image
import photo_mosaic.util


class TestUtil(TestCase):
    """ Test case for util module """

    def test_get_image_names(self):
        eq_(7, len(photo_mosaic.util.get_image_names('./test')))

    def test_convert_to_rgb_image(self):
        img_names = photo_mosaic.util.get_image_names('./test')
        for img_name in img_names:
            img = Image.open(img_name)
            img = photo_mosaic.util.convert_to_rgb_image(img)
            eq_('RGB', img.mode)

    def test_trim_into_square(self):
        img_names = photo_mosaic.util.get_image_names('./test')
        for img_name in img_names:
            img = Image.open(img_name)
            img = photo_mosaic.util.convert_to_rgb_image(img)
            short_side = min(img.size)
            img = photo_mosaic.util.trim_into_square(img)
            eq_(img.size[0], img.size[1])
            eq_(short_side, img.size[0])

