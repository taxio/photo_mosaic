from PIL import Image, ImageStat
import glob


if __name__ == '__main__':
    img_names = glob.glob('./images/*')
    for img_name in img_names:
        img = Image.open(img_name)
        # 透過画像の場合は一度RGBAに変換
        if "transparency" in img.info:
            img = img.convert("RGBA")
        img = img.convert("RGB")
        stat = ImageStat.Stat(img)
        print(img_name, stat.mean)
