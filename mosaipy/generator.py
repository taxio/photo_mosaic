from PIL import Image, ImageStat
import numpy as np
import sqlite3
from progressbar import ProgressBar


class PhotoMosaicGenerator:

    def __init__(self, materials_db: str):
        # データベースから一覧取得
        conn = sqlite3.connect(materials_db)
        c = conn.cursor()
        c.execute('select * from images')
        self._materials = c.fetchall()
        conn.close()

    def generate(self, target_image_name: str, n_split: int, output_image_name: str):
        print('generating photo mosaic...')

        target_image = Image.open(target_image_name)
        target_image_size = target_image.size
        mat_size = target_image_size[0] // n_split
        target_image = np.array(target_image, 'f')
        print(target_image_name, target_image.shape)

        pbar = ProgressBar(max_value=n_split*n_split)
        gen_image = Image.new('RGB', target_image_size, 'white')
        v_imgs = np.array_split(target_image, n_split, axis=1)
        for n_v, v in enumerate(v_imgs):
            h_imgs = np.array_split(v, n_split, axis=0)
            for n_h, h in enumerate(h_imgs):
                # 対象画像の平均値計算
                tmp_mean = np.mean(h, axis=0)
                tmp_mean = np.mean(tmp_mean, axis=0)
                # 近似画像取得
                mat_img = self.get_near_image(tmp_mean[0], tmp_mean[1], tmp_mean[2])
                # 近似画像を指定位置に貼り付け
                mat_image = Image.open(mat_img)
                if "transparency" in mat_image.info:
                    mat_image = mat_image.convert("RGBA")
                mat_image = mat_image.convert("RGB")
                mat_image = self.trim_into_square(mat_image)
                mat_image = mat_image.resize((mat_size, mat_size))
                gen_image.paste(mat_image, (n_v*mat_size, n_h*mat_size))
                # print(n_v, n_h, mat_img, mat_image.size)
                pbar.update(n_v*n_split+n_h)

        gen_image.save(output_image_name)
                

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


    def get_near_image(self, r, g, b, threshold=10):
        """
        指定のRGB値からもっとも近い画像を返す
        しきい値内に収まっている画像が複数存在する場合はランダムで返す
        """

        base_point = np.array([r, g, b])
        candidates = list()
        for m in self._materials:
            m_point = np.array([m[2], m[3], m[4]])
            diff = np.linalg.norm(base_point-m_point)
            candidates.append([m[1], diff])

        candidates.sort(key=lambda x:x[1])

        for idx, m in enumerate(candidates):
            if m[1] > threshold:
                break
        return candidates[np.random(idx)][0]

