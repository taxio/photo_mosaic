from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, REAL
import glob
import os, imghdr, shutil
from PIL import Image, ImageStat
from progressbar import ProgressBar

class ImportImages:

    def __init__(self, dbname: str, img_dir_path: str):
        self._dbname = dbname
        self._img_dir_path = img_dir_path

    def _get_image_names(self):
        img_names = list()
        for (root, dirs, files) in os.walk(self._img_dir_path): # 再帰的に探索
            for f in files: # ファイル名だけ取得
                target = os.path.join(root,f).replace("\\", "/")  # フルパス取得
                if os.path.isfile(target): # ファイルかどうか判別
                    if imghdr.what(target) != None : # 画像ファイルかどうかの判別
                        img_names.append(target) # 画像ファイルであればリストに追加
        return img_names

    def _create_table(self):
        self._engine = create_engine('sqlite:///'+self._dbname, echo=False)
        self._metadata = MetaData()
        self._metadata.bind = self._engine

        self._images = Table(
                'images', self._metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String),
                Column('R', REAL),
                Column('G', REAL),
                Column('B', REAL)
                )

        self._metadata.create_all()

    def calc_mean(self):
        self._create_table()
        image_names = self._get_image_names()
        n_img = len(image_names)
        pbar = ProgressBar(max_value=len(image_names))
        for idx, img_name in enumerate(image_names):
            pbar.update(idx)
            try:
                img = Image.open(img_name)
            except OSError as e:
                continue
            # 透過画像の場合は一度RGBAに変換
            if "transparency" in img.info:
                img = img.convert("RGBA")
            img = img.convert("RGB")
            stat = ImageStat.Stat(img)
            self._images.insert().execute(name=img_name, R=stat.mean[0], G=stat.mean[1], B=stat.mean[2])
        pbar.finish()


