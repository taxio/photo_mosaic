from PIL import Image, ImageStat
import numpy as np
import sqlite3


class PhotoMosaicGenerator:

    def __init__(self, target_image: str, materials_db: str):
        self._target = target_image

        # データベースから一覧取得
        conn = sqlite3.connect(materials_db)
        c = conn.cursor()
        c.execute('select * from images')
        self._materials = c.fetchall()
        conn.close()

    def generate(self, n_split: int):
        print('generating photo mosaic...')

        target_image = Image.open(self._target)
        target_image_size = target_image.size
        mat_size = target_image_size[0] // n_split
        target_image = np.array(target_image, 'f')
        print(self._target, target_image.shape)

        # means = list()  # 分割したRGB値平均値がここに入る
        materials = list()
        v_imgs = np.array_split(target_image, n_split, axis=1)
        for v in v_imgs:
            tmp = list()
            material = list()
            h_imgs = np.array_split(v, n_split, axis=0)
            for h in h_imgs:
                tmp_mean = np.mean(h, axis=0)
                tmp_mean = np.mean(tmp_mean, axis=0)
                mat_img = self.get_near_image(tmp_mean[0], tmp_mean[1], tmp_mean[2])
                tmp.append(tmp_mean)
                print(mat_img)
                material.append(mat_img)

            # means.append(tmp)
            materials.append(material)

        # 画像貼り付け
        gen_image = Image.new('RGB', target_image_size, 'white')
        for n_v, mats in enumerate(materials):
            for n_h, mat in enumerate(mats):
                mat_image = Image.open(mat)
                if "transparency" in mat_image.info:
                    mat_image = mat_image.convert("RGBA")
                mat_image = mat_image.convert("RGB")
                mat_image = self.trim_into_square(mat_image)
                mat_image = mat_image.resize((mat_size, mat_size))
                print(n_v, n_h, mat, mat_image.size)
                gen_image.paste(mat_image, (n_v*mat_size, n_h*mat_size))

        gen_image.save('generated.png')
                

    def trim_into_square(self, img):
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


    def get_near_image(self, r, g, b):

        base_point = np.array([r, g, b])
        buf_calc = list()
        for m in self._materials:
            m_point = np.array([m[2], m[3], m[4]])
            diff = np.linalg.norm(base_point-m_point)
            buf_calc.append([m[1], diff])

        # ソート
        buf_calc.sort(key=lambda x:x[1])
        return buf_calc[0][0]

