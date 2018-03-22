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
        target_image = np.array(target_image, 'f')
        print(self._target, target_image.shape)

        means = list()  # 分割したRGB値平均値がここに入る
        v_imgs = np.array_split(target_image, n_split, axis=1)
        for v in v_imgs:
            tmp = list()
            h_imgs = np.array_split(v, n_split, axis=0)
            for h in h_imgs:
                tmp_mean = np.mean(h, axis=0)
                tmp_mean = np.mean(tmp_mean, axis=0)
                mat_img = self.get_near_image(tmp_mean[0], tmp_mean[1], tmp_mean[2])
                tmp.append(tmp_mean)
                print(mat_img)

            means.append(tmp)

        print(len(means), len(means[0]))


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

