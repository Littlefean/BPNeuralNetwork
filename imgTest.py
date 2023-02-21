"""
精灵图切图测试
此图用于将大图切割成很多小图片并依次存放到img文件夹中。
"""

from PIL import Image

LEN = 28  # 小图片的宽度和高都是 28
WIDTH = 75  # 一行里有75 个小图片
HEIGHT = 65  # 至少有65行


# 一个数字至少有 4875 张


def getImg(im, x, y, fileName):
    """从im原图中切出一小块图"""
    left = x * LEN
    top = y * LEN
    box = (left, top, (x + 1) * LEN, (y + 1) * LEN)
    dig_img = im.crop(box)
    dig_img.save(f"img/{fileName}.jpg")
    # res_img = Image.new("RGB", (LEN, LEN), (30, 0, 0))
    # res_img.paste(dig_img, box, mask=0)
    # res_img.save(f"img/{fileName}.jpg")


def main():
    im = Image.open("training_data.jpg")
    print(im.height)
    print(18676 / LEN)
    print(WIDTH * HEIGHT)
    count = 0
    for y in range(667):
        for x in range(WIDTH):
            getImg(im, x, y, count)
            count += 1
            print(x, y)
    return None


if __name__ == "__main__":
    main()
