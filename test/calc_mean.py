from PIL import Image, ImageStat
import glob


if __name__ == '__main__':
    img_names = glob.glob('./images/*')
    for img_name in img_names:
        img = Image.open(img_name).convert("RGB")
        stat = ImageStat.Stat(img)
        print(img_name, stat.mean)