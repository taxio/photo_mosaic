from PIL import Image
import os, imghdr, shutil

def trim_into_square(img: Image):
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

    return img

def convert_to_rgb_image(img: Image):
    if "transparency" in img.info:
        img = img.convert("RGBA")
    img = img.convert("RGB")
    return img

def get_image_names(img_dir_path):
    print('searching images...')
    img_names = list()
    for (root, dirs, files) in os.walk(img_dir_path): # 再帰的に探索
        for f in files: # ファイル名だけ取得
            target = os.path.join(root,f).replace("\\", "/")  # フルパス取得
            if os.path.isfile(target): # ファイルかどうか判別
                if imghdr.what(target) != None : # 画像ファイルかどうかの判別
                    img_names.append(target) # 画像ファイルであればリストに追加
    print('got images')
    return img_names
