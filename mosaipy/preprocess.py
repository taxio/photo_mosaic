from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, REAL
from PIL import Image, ImageStat
from progressbar import ProgressBar
import mosaipy.util

class ImportImages:

    def __init__(self, dbname: str, img_dir_path: str):
        self._dbname = dbname
        self._img_dir_path = img_dir_path

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
        # inserts = list()
        print('calculation images start')
        pbar = ProgressBar(max_value=len(image_names))
        for idx, img_name in enumerate(image_names):
            pbar.update(idx)
            try:
                img = Image.open(img_name)
            except OSError as e:
                continue
            img = mosaipy.util.convert_to_rgb_image(img)
            img = mosaipy.util.trim_into_square(img)
            stat = ImageStat.Stat(img)
            # tmp_insert = [img_name, stat.mean[0], stat.mean[1], stat.mean[2]]
            # inserts.append(tmp_insert)
            self._images.insert().execute(name=img_name, R=stat.mean[0], G=stat.mean[1], B=stat.mean[2])
        pbar.finish()
        print('finish')

