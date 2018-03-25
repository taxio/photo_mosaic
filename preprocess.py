from PIL import Image, ImageStat
from progressbar import ProgressBar
import photo_mosaic.util
from photo_mosaic import dbmanager


class PreProcess:

    def __init__(self, dbname: str):
        self._db = dbmanager.DBManager(dbname=dbname)

    def drop_table(self):
        self._db.drop_table()
    
    def insert_image(self, img_name):
        new_material = self.calc_mean(img_name)
        if new_material:
            self._db.insert_material(new_material)

    def calc_mean(self, img_name):
        try:
            img = Image.open(img_name)
        except OSError as e:
            return None
        img = photo_mosaic.util.convert_to_rgb_image(img)
        img = photo_mosaic.util.trim_into_square(img)
        stat = ImageStat.Stat(img)

        new_material = dbmanager.MaterialImage(name=img_name, R=stat.mean[0], G=stat.mean[1], B=stat.mean[2])
        return new_material

    def calc_all(self, img_dir_path: str):
        image_names = photo_mosaic.util.get_image_names(img_dir_path)
        print('calculation images start')
        pbar = ProgressBar(max_value=len(image_names))
        new_materials = list()
        for idx, image_name in enumerate(image_names):
            pbar.update(idx)
            new_material = self.calc_mean(image_name)
            if new_material:
                new_materials.append(new_material)

        self._db.insert_all_material(new_materials)
        pbar.finish()
        print('finish')

