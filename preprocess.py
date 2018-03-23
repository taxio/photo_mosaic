from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, REAL
from PIL import Image, ImageStat
from progressbar import ProgressBar
import photo_mosaic.util

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class MaterialImage(Base):
    
    __tablename__ = 'materials'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    R = Column(REAL)
    G = Column(REAL)
    B = Column(REAL)

    def __repr__(self):
        return '<Material(name=\'{}\', (R, G, B)=({}, {}, {}))>'.format(name, R, G, B)

class ImportImages:

    def __init__(self, dbname: str, img_dir_path: str):
        self._dbname = dbname
        self._img_dir_path = img_dir_path
        self._engine = create_engine('sqlite:///'+dbname, echo=False)
        Base.metadata.create_all(self._engine)

    def drop_table(self):
        Base.metadata.drop_all(self._engine)

    def calc_mean(self):
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
            img = photo_mosaic.util.convert_to_rgb_image(img)
            img = photo_mosaic.util.trim_into_square(img)
            stat = ImageStat.Stat(img)
            # tmp_insert = [img_name, stat.mean[0], stat.mean[1], stat.mean[2]]
            # inserts.append(tmp_insert)
            self._images.insert().execute(name=img_name, R=stat.mean[0], G=stat.mean[1], B=stat.mean[2])
        pbar.finish()
        print('finish')

