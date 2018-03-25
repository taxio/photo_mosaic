# photo_mosaic
素材画像から目的の画像のフォトモザイクを作成する

## Requirements

- Python 3.5 or later
- nose==1.3.7
- numpy==1.14.2
- Pillow==5.0.0
- progressbar2==3.36.0
- SQLAlchemy==1.2.5

pip install

```Bash
pip install -r requirements.txt
```

## Usage

```Python
from photo_mosaic import PhotoMosaicGenerator, PreProcess

if __name__ == '__main__':

    pre = PreProcess(dbname='./test.sqlite3')
    pre.calc_all('./images')

    gen = PhotoMosaicGenerator(materials_db='./test.sqlite3')
    gen.generate(
            target_image_name='target.png',
            output_image_name='output.png',
            n_split=4)
```

指定ディレクトリ以下にある画像を全て読み込み，そのRGB平均値をSQLiteデータベースに落とし込みます．

データベースには各画像へのパスが登録されているため，前処理後に画像を移動させると正しく計算することができません．

## License

MIT