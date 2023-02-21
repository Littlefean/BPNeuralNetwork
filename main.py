# -*- encoding: utf-8 -*-
"""
运行主文件
"""
# 一行有 75 个小图片
# 0 有 66 行，不足66行
# 一个小图片的大小是 28*28

# 先看看每个数字都有多少张图片
from time import perf_counter
import os
from PIL import Image
from net import Net
from dataSet import DataSet


def main():
    for i in range(10):
        arr = os.listdir(f"img-{i}")
        print(len(arr))
    ...
    # nt = Net()
    nt = Net.getNetFromFile("2023-2-19-测试1")
    ds = DataSet()

    # ------------训练 0~9 十个数字输入完就改一次权重，总共100组
    # trainGroup = 4000
    # for i in range(trainGroup):
    #     for number in range(10):
    #         nt.inputKnowAndChange(Image.open(f"img-{number}/{ds.getIndex(number)}.jpg"), number)
    #         ds.add(number)
    #     # nt.changeWeightAndBias()
    #     nt.saveCurrentNetImage(i)  # 更改完了顺便保存一次图片
    #     print(f"已经完成{i}轮训练，总共{trainGroup}组")

    # ------------测试 10组，每组都是0~9数字
    rightCount = 0  # 打对的数量
    for i in range(10):
        print(f"正在进行第{i}轮测试")
        print()
        for number in range(10):
            print(f"网络输入了一个数字为{number}的图片，图片编号为{ds.getIndex(number)}：")
            nt.inputImg(Image.open(f"img-{number}/{ds.getIndex(number)}.jpg"))
            nt.leftToRight()  # 笑死，少了一行代码
            ds.add(number)
            nt.showResult()
            res = nt.getResult()
            if res == number:
                rightCount += 1
    print("正确率：", rightCount / 100)

    nt.saveNetToFile("2023-2-19-测试1")

    # ========= 手动测试
    while True:
        nt.inputImg(Image.open("write.png"))
        nt.leftToRight()
        nt.showInputImgMatrix()
        nt.showResult()
        input("结束，Enter继续")


if __name__ == "__main__":
    t1 = perf_counter()
    main()
    t2 = perf_counter()
    sec = t2 - t1
    minute = sec / 60
    print("程序用时", minute, "分钟")
