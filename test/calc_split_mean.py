from PIL import Image, ImageStat
import numpy as np
import time

N_SPLIT = 1000

if __name__ == '__main__':
    img_name = './images/aqua.JPG'
    img = Image.open(img_name)
    img = np.array(img, 'f')
    print(img.shape)

    means = list()  # 分割したRGB値平均値がここに入る
    v_imgs = np.array_split(img, N_SPLIT, axis=1)
    for v in v_imgs:
        tmp = list()
        h_imgs = np.array_split(v, N_SPLIT, axis=0)
        for h in h_imgs:
            tmp_mean = np.mean(h, axis=0)
            tmp_mean = np.mean(tmp_mean, axis=0)
            tmp.append(tmp_mean)

        means.append(tmp)

