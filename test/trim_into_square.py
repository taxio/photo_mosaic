from PIL import Image
import numpy as np

if __name__ == '__main__':

    img = Image.open('./test/images/aqua.JPG')
    print(img.size)
    square_size = min(img.size)
    width, height = img.size

    if width > height:
        top = 0
        bottom = square_size
        left = (width - square_size) / 2
        right = left + square_size
        box = (left, top, right, bottom)
    else:
        left = 0
        right = square_size
        top = (height - square_size) / 2
        bottom = top + square_size
        box = (left, top, right, bottom)

    img = img.crop(box)

    thumbnail_size = (square_size, square_size)
    img.thumbnail(thumbnail_size)
    print(img.size)
    img.save('square_sample.jpg', 'JPEG')
    

