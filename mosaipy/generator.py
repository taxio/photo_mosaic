from PIL import Image, ImageStat
import numpy as np


class PhotoMosaicGenerator:

    def __init__(self, target_image: str, materials_db: str):
        self._target = target_image
        self._dbname = materials_db

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
                tmp.append(tmp_mean)

            means.append(tmp)

        print(len(means), len(means[0]))
