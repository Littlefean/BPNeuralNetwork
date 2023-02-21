from random import random, uniform, gauss
from PIL import Image

from copy import deepcopy
from imgSave import tableToImage
from myMath import *


class Net:
    """神经网络类"""

    def __init__(self):
        # 学习率
        self.studyRate = 0.025
        # 正确的目标亮度值
        self.trueValue = 0.999
        # 错误的目标亮度值
        self.falseValue = 0.001

        # 所有的节点列表示的数组
        # 第一个元素表示输入层的节点数量，
        # 最后一个元素表示输出层的节点数量
        # 所有的中间元素表示隐含层
        self.layerCountArr = [28 * 28, 16, 16, 10]

        # 里面的每个线段权重都是二维表，二维数组表示权重
        self._weightArray: List[List[List[float]]] = []

        # 临时记录所有点亮的节点的值，包涵了第一层
        self._tempNodeLightList: List[List[float]] = []  # 存放点亮的节点，有第一层

        # 每个节点头顶上有一个缓存误差值
        self._errNodeLightList: List[List[float]] = []  # 存放点亮的节点，有第一层

        self._arrInit()

        ...

    def _arrInit(self):
        """给所有的高纬数组初始化"""
        arr = self.layerCountArr
        for i, n in enumerate(arr):
            # 构建临时点亮节点数组
            self._tempNodeLightList.append([0] * n)
            # 构建临时误差数组
            self._errNodeLightList.append([0] * n)

            if i == 0:
                continue
            height = arr[i - 1]
            width = n
            # 权值随机范围是在 -1/✓n ~ 1/✓n

            weightLayer = [
                # [uniform(-1 / (n ** 0.5), 1 / (n ** 0.5)) for _ in range(width)] for _ in range(height)
                [gauss(0, 1 / (n ** 0.5)) for _ in range(width)] for _ in range(height)
            ]
            self._weightArray.append(weightLayer)

    def __dict__(self):
        """将这个网络转成可以保存的对象，用于保存内部结构"""
        return {
            "layerCountArr": self.layerCountArr,
            "_weightArray": self._weightArray,
            "_tempNodeLightList": self._tempNodeLightList,
            "_errNodeLightList": self._errNodeLightList,
            # 学习率
            "studyRate": self.studyRate,
            # 正确的目标亮度值
            "trueValue": self.trueValue,
            # 错误的目标亮度值
            "falseValue": self.falseValue,
        }

    def saveNetToFile(self, fileName):
        """把当前的网络保存到saveNet文件夹下"""
        with open(f"saveNet/{fileName}.py", "w", encoding="utf-8") as f:
            f.write(repr(self.__dict__()))

    @classmethod
    def getNetFromFile(cls, fileName):
        """打开一个网络"""
        with open(f"saveNet/{fileName}.py", encoding="utf-8") as f:
            dicStr = f.read()
        dic = eval(dicStr)
        res = cls()
        res.trueValue = dic["trueValue"]
        res.falseValue = dic["falseValue"]
        res.studyRate = dic["studyRate"]
        res.layerCountArr = dic["layerCountArr"]
        res._weightArray = dic["_weightArray"]
        res._tempNodeLightList = dic["_tempNodeLightList"]
        res._errNodeLightList = dic["_errNodeLightList"]
        return res

    def saveCurrentNetImage(self, number: int):
        """保存当前的网络内部状态，生成一个图片"""
        # 先保存权重值
        for i, table in enumerate(self._weightArray):
            tableToImage(table).save(f"netImg/第{i}层权值/{str(number).zfill(5)} 轮训练.png")
        ...

    def input(self, arr: list):
        # 输入一个一维数组 长度刚好是
        assert len(arr) == self.layerCountArr[0]
        # 直接填充第一层
        for i, n in enumerate(arr):
            self._tempNodeLightList[0][i] = n

    def leftToRight(self):
        """
        从左到右扩散传播，此时的暂存是已经填好了的
        一般在此之前会调用input函数
        :return:
        """
        for layerIndex, leftArr in enumerate(self._tempNodeLightList):
            if layerIndex == len(self._tempNodeLightList) - 1:
                # 已经到了最后一层了，不能再向下传播了
                break
            # leftArr 左侧一列神经元  nextArr 右侧一列神经元
            rightArr = self._tempNodeLightList[layerIndex + 1]

            # 遍历左侧每个神经元 ai
            for i, a in enumerate(leftArr):
                # 遍历右侧每个神经元 bj
                for j, b in enumerate(rightArr):
                    # 开始累加数字
                    # 亮度乘以权重
                    self._tempNodeLightList[layerIndex + 1][j] += self._getWeight(layerIndex, i, j) * a

                ...
            # 累加完了之后开始对右边统计进行 sigmoid(x + 偏置)
            for i, sumNumber in enumerate(rightArr):
                # rightArr[i] = sigmoid(x + self._getBias(layerIndex + 1, i))
                rightArr[i] = sigmoid(sumNumber)
        # 最终填好的数字就到最右侧了
        ...

    def showNode(self):
        """打印当前网络的点亮状态"""
        for arr in self._tempNodeLightList:
            print(arr)
            # for n in arr:
            #     strN = str(n)
            #     if "." in strN:
            #         z, x = strN.split(".")
            #         print(f"{z}.{x[:2]}", end="\t")
            #     else:
            #         print(n, end="\t")
        print("=" * 50)

    def showResult(self):
        """打印当前网络结果层的点亮状态"""
        for i, n in enumerate(self._tempNodeLightList[-1]):
            print(f"[{i}] {round(n, 3)}", end="\t")
        print()
        print("-" * 50)

    def getResult(self):
        """获取当前网络得到的结果"""
        maxLight = -float("INF")
        maxIndex = 0
        for y in range(self.layerCountArr[-1]):
            lightness = self._getNodeLight(len(self.layerCountArr) - 1, y)
            if lightness > maxLight:
                maxLight = lightness
                maxIndex = y
        return maxIndex

    def showInner(self):
        """展示网络的内部结构，所有的偏和权"""
        print("========")
        for table in self._weightArray:
            for line in table:
                print(line)
            print()
        # print("偏重：")
        # for col in self._biasArray:
        #     print(col)
        print("--------")

    def _getNodeLight(self, colIndex, i):
        """获取某一个位置上节点的亮度"""
        return self._tempNodeLightList[colIndex][i]

    def _getNodeErr(self, colIndex, i):
        """获取某一个位置上节点的误差值"""
        return self._errNodeLightList[colIndex][i]

    def _setNodeErr(self, colIndex, i, value):
        """设置某一个位置节点的误差值"""
        self._errNodeLightList[colIndex][i] = value

    def _getWeight(self, leftLayer, i, j):
        """
        获取权重
        :param leftLayer: 从左边列出发，左边列的列编号是多少
        :param i: 左列的第多少个节点
        :param j: 右侧列的第几个节点
        网络示意图
        → a  b →
        → c  d →
        [
            [a→b   a→d],
            [c→b   c→d],
        ]
        [
            [w11   w12],
            [w21   w22],
        ] 与python神经网络那本书上刚好是转置的对应关系
        :return:
        """
        return self._weightArray[leftLayer][i][j]

    def _setWeight(self, leftLayer, i, j, value):
        """更改一条权重"""
        self._weightArray[leftLayer][i][j] = value

    def _getWeightMatrix(self, leftLayer):
        """获取权重矩阵，这个和书上是一致的，不是转置的"""
        return matrixTrans(self._weightArray[leftLayer])

    def inputImg(self, im: Image):
        """输入一张灰度图"""
        arr = []
        for y in range(im.height):
            for x in range(im.width):
                tup = im.getpixel((x, y))
                if len(tup) == 3:
                    r, g, b = tup
                    arr.append((r + g + b) // 3 / 255)
                elif len(tup) == 4:
                    r, g, b, a = tup
                    arr.append((r + g + b) // 3 / 255)
        self.input(arr)

    def showInputImgMatrix(self):
        # 默认图片是正方形的
        length = int(self.layerCountArr[0] ** 0.5)
        for y in range(length):
            for x in range(length):
                m = self._getNodeLight(0, y * length + x)
                if m == 0.0:
                    print(" . ", end="  ")
                else:
                    print(round(m, 3), end="  ")
            print()

    def inputKnowAndChange(self, im: Image, number: int):
        """
        传入一个已经知道是数字几的图片
        并反向传播填写期待更改的数字
        反向传播误差，然后更改每一个权重
        """
        self.inputImg(im)
        self.leftToRight()
        rightIndex = len(self.layerCountArr) - 1
        # ===== 更新每一层节点头顶上的误差数字
        # 先更新最右侧的
        for n in range(self.layerCountArr[-1]):  # 0123456789
            light = self._getNodeLight(rightIndex, n)  # 遍历获取最右侧节点的亮度

            if n == number:
                e = self.trueValue - light
            else:
                e = self.falseValue - light
            self._setNodeErr(rightIndex, n, e)
        for i in reversed(range(rightIndex)):  # 0 1 ... rightIndex-1    反着来
            m = self._getWeightMatrix(i)
            v = self._errNodeLightList[i + 1]
            v1 = matrixMul(matrixTrans(m), v)
            for j, n in enumerate(v1):
                self._setNodeErr(i, j, n)
        # =====

        # 对每一条权重 进行求梯度，更改
        for leftLayer in range(len(self.layerCountArr) - 1):
            # 遍历每一个左竖列 ，最右边不需要 所以 -1
            for i in range(self.layerCountArr[leftLayer]):
                leftLight = self._getNodeLight(leftLayer, i)

                for j in range(self.layerCountArr[leftLayer + 1]):
                    oldW = self._getWeight(leftLayer, i, j)
                    rightLight = self._getNodeLight(leftLayer + 1, j)
                    rightErr = self._getNodeErr(leftLayer + 1, j)
                    rate = -rightErr * rightLight * (1 - rightLight) * leftLight
                    self._setWeight(leftLayer, i, j, oldW - self.studyRate * rate)
                    # todo 每输入一个数字图片就整体更改一次权重，可能会出现打架的问题

            ...

    ...
