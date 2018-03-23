from PIL import Image, ImageStat
import numpy as np
import sqlite3
from progressbar import ProgressBar
import photo_mosaic.util


class PhotoMosaicGenerator:

    def __init__(self, materials_db: str):
        # データベースから一覧取得
        conn = sqlite3.connect(materials_db)
        c = conn.cursor()
        c.execute('select * from images')
        self._materials = c.fetchall()
        conn.close()

    def generate(self, target_image_name: str, n_split: int, output_image_name: str, threshold_near=5):
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
                mat_img = self.get_near_image(tmp_mean[0], tmp_mean[1], tmp_mean[2], threshold=threshold_near)
                # 近似画像を指定位置に貼り付け
                mat_image = Image.open(mat_img)
                mat_image = photo_mosaic.util.convert_to_rgb_image(mat_image)
                mat_image = photo_mosaic.util.trim_into_square(mat_image)
                mat_image = mat_image.resize((mat_size, mat_size))
                gen_image.paste(mat_image, (n_v*mat_size, n_h*mat_size))
                # print(n_v, n_h, mat_img, mat_image.size)
                pbar.update(n_v*n_split+n_h)

        gen_image.save(output_image_name)

    def get_near_image(self, r, g, b, threshold):
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

        most_near_diff = candidates[0][1]
        for idx, m in enumerate(candidates):
            if (m[1]-most_near_diff) > threshold:
                break
        if idx == 0:
            idx = 1
        return candidates[np.random.randint(idx)][0]
