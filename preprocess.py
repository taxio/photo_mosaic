from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, REAL
from PIL import Image, ImageStat
from progressbar import ProgressBar
import photo_mosaic.util

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import sessionmaker


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

    def __init__(self, dbname: str):
        self._dbname = dbname
        self._engine = create_engine('sqlite:///'+dbname, echo=False)
        Base.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()

    def close_session(self):
        self._session.close()

    def drop_table(self):
        Base.metadata.drop_all(self._engine)
    
    def insert_image(self, img_name):
        new_material = self.calc_mean(img_name)
        if new_material:
            self._session.add(new_material)
            self._session.commit()

    def calc_mean(self, img_name):
        try:
            img = Image.open(img_name)
        except OSError as e:
            return None
        img = photo_mosaic.util.convert_to_rgb_image(img)
        img = photo_mosaic.util.trim_into_square(img)
        stat = ImageStat.Stat(img)

        new_material = MaterialImage(name=img_name, R=stat.mean[0], G=stat.mean[1], B=stat.mean[2])
        return new_material

    def calc_all(self, img_dir_path: str):
        image_names = photo_mosaic.util.get_image_names(img_dir_path)
        print('calculation images start')
        pbar = ProgressBar(max_value=len(image_names))
        for idx, image_name in enumerate(image_names):
            pbar.update(idx)
            new_material = self.calc_mean(image_name)
            if new_material:
                self._session.add(new_material)

        self._session.commit()
        pbar.finish()
        print('finish')

