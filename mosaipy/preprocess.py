from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, REAL
import glob
from PIL import Image, ImageStat

class ImportImages:

    def __init__(self, dbname: str, img_dir_path: str):
        self._dbname = dbname
        self._img_dir_path = img_dir_path

    def _get_image_names(self):
        imgs = glob.glob(self._img_dir_path+'/*')
        return imgs

    def _create_table(self):
        self._engine = create_engine('sqlite:///'+self._dbname, echo=True)
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
        for img_name in image_names:
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


