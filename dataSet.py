"""
此模块只存放一个 数据集 记录类
"""


class DataSet:
    # 每个数字对应的图片数量
    countDic = {
        0: 4932,
        1: 5678,
        2: 4968,
        3: 5101,
        4: 4859,
        5: 4506,
        6: 4951,
        7: 5175,
        8: 4842,
        9: 4988,
    }
    startIndexDic = {
        0: 0,
        1: 4932,
        2: 10610,
        3: 15578,
        4: 20679,
        5: 25538,
        6: 30044,
        7: 34995,
        8: 40170,
        9: 45012,
    }

    def __init__(self):
        # 记录起始位置下标
        self.index = [DataSet.startIndexDic[i] for i in range(10)]
        ...

    def add(self, number):
        self.index[number] += 1

    def getIndex(self, number):
        return self.index[number]

    ...
