from PIL import Image, ImageStat
import numpy as np
from progressbar import ProgressBar

import photo_mosaic.util
from photo_mosaic import dbmanager


class PhotoMosaicGenerator:

    def __init__(self, materials_db: str):
        self._db = dbmanager.DBManager(dbname=materials_db)
        self._materials = self._db.get_materials()

    def generate(self, target_image_name: str, n_split: int, output_image_name: str, threshold_near=5):
        print('generating photo mosaic...')

        target_image = Image.open(target_image_name)
        target_image = photo_mosaic.util.convert_to_rgb_image(target_image)
        gen_image = Image.new('RGB', target_image.size, 'white')
        mat_size = gen_image.size[0] // n_split
        target_image = np.array(target_image, 'f')
        print(target_image_name, target_image.shape)

        pbar = ProgressBar(max_value=n_split*n_split)
        v_imgs = np.array_split(target_image, n_split, axis=1)
        for n_v, v in enumerate(v_imgs):
            h_imgs = np.array_split(v, n_split, axis=0)
            for n_h, h in enumerate(h_imgs):
                # 対象画像の平均値計算
                mean = np.mean(h, axis=0)
                mean = np.mean(mean, axis=0)
                # 近似画像取得
                mat_image_name = self.get_near_image_name(mean, threshold=threshold_near)
                # 近似画像を指定位置に貼り付け
                mat_image = Image.open(mat_image_name)
                mat_image = photo_mosaic.util.convert_to_rgb_image(mat_image)
                mat_image = photo_mosaic.util.trim_into_square(mat_image)
                mat_image = mat_image.resize((mat_size, mat_size))
                gen_image.paste(mat_image, (n_v*mat_size, n_h*mat_size))

                pbar.update(n_v*n_split+n_h)

        gen_image.save(output_image_name)

    def get_near_image_name(self, rgb, threshold):
        """
        指定のRGB値からもっとも近い画像を返す
        しきい値内に収まっている画像が複数存在する場合はランダムで返す
        """

        base_point = np.array(rgb)
        candidates = list()
        for mat in self._materials:
            m_point = np.array([mat.R, mat.G, mat.B])
            diff = np.linalg.norm(base_point-m_point)
            candidates.append([mat.name, diff])

        candidates.sort(key=lambda x:x[1])

        most_near_diff = candidates[0][1]
        for idx, mat in enumerate(candidates):
            if (mat[1]-most_near_diff) > threshold:
                break
        if idx == 0:
            idx = 1
        return candidates[np.random.randint(idx)][0]

