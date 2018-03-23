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

    def __init__(self, dbname: str, img_dir_path: str):
        self._dbname = dbname
        self._img_dir_path = img_dir_path
        self._engine = create_engine('sqlite:///'+dbname, echo=False)
        Base.metadata.create_all(self._engine)

    def drop_table(self):
        Base.metadata.drop_all(self._engine)

    def calc_mean(self):
        image_names = photo_mosaic.util.get_image_names(self._img_dir_path)
        print('calculation images start')
        Session = sessionmaker(bind=self._engine)
        session = Session()
        pbar = ProgressBar(max_value=len(image_names))
        for idx, image_name in enumerate(image_names):
            pbar.update(idx)
            try:
                img = Image.open(image_name)
            except OSError as e:
                continue
            img = photo_mosaic.util.convert_to_rgb_image(img)
            img = photo_mosaic.util.trim_into_square(img)
            stat = ImageStat.Stat(img)

            new_material = MaterialImage(name=image_name, R=stat.mean[0], G=stat.mean[1], B=stat.mean[2])
            session.add(new_material)

        session.commit()
        session.close()
        pbar.finish()
        print('finish')

