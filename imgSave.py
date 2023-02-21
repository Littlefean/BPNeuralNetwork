"""
此模块专门用于将数据保存成图片，方便查找bug

"""
import math
from typing import *
from PIL import Image, ImageDraw


def valueToColor(value) -> Tuple[int, int, int]:
    _y = int(math.atan(value) / math.pi * 255)
    r, g, b = 0, 0, 0
    if _y > 0:
        r = _y
    else:
        b = -_y
    return r, g, b


def tableToImage(table: List[List[float]], imgH=1000, imgW=1000) -> Image:
    """
    将二维数组转化成一个图片对象
    转化成 1024 * 1024 的正方形图片
    :param imgH:
    :param imgW:
    :param table:
    :return:
    """
    h, w = len(table), len(table[0])
    im = Image.new("RGB", (imgW, imgH), 0)
    draw = ImageDraw.ImageDraw(im)

    rectW = imgW / w
    rectH = imgH / h
    for y in range(h):
        for x in range(w):
            # 遍历二维矩阵
            # im.putpixel((x, y), valueToColor(table[y][x]))

            draw.rectangle(
                (int(x * rectW), int(y * rectH), int((x + 1) * rectW), int((y + 1) * rectH)),
                fill=valueToColor(table[y][x])
            )
    return im


def main():
    w = 16
    h = 3
    arr = [[0] * w for _ in range(h)]
    arr = [
        [6, 9, 4, 2],
        [-6, 9, -4, 2],
        [6, 9, 4, 2],
        [6, -9, 4, -20],
    ]
    tableToImage(arr).show()


if __name__ == "__main__":
    main()
