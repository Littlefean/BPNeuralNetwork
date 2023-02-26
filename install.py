"""
自动安装脚本
"""

import ctypes
import psutil
import os
import shutil
import time
import pip
from PIL import Image


def get_file_system(label: str):
    """
    获取文件系统
    """
    pts = psutil.disk_partitions()
    for pt in pts:
        if pt.device.startswith(label.upper()):
            return pt.fstype


def get_free_space_mb(label: str):
    """
    获取磁盘剩余空间，单位mb
    """
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(
        label + ":\\"), None, None, ctypes.pointer(free_bytes))
    return free_bytes.value / 2 ** 20


disk = __file__[0]
file_system = get_file_system(disk)
free_space = get_free_space_mb(disk)
space_required = 200 * 2 if file_system == "NTFS" else 400 * 2
images = {
    0: range(0, 4932),
    1: range(4932, 10610),
    2: range(10610, 15578),
    3: range(15578, 20679),
    4: range(20679, 25538),
    5: range(25538, 30044),
    6: range(30044, 34995),
    7: range(34995, 40170),
    8: range(40170, 45012),
    9: range(45012, 50025),
}
dirs = [
    "img",
    "img-0",
    "img-1",
    "img-2",
    "img-3",
    "img-4",
    "img-5",
    "img-6",
    "img-7",
    "img-8",
    "img-9",
]

print("盘符", disk)
print("文件系统", file_system)
print("剩余空间(MB)", free_space)
print()

time1 = time.time()

for dir in dirs:
    if not os.path.isdir(dir):
        print(dir, "目录不存在，创建")
        os.mkdir(dir)

print("运行imgTest")
with open("imgTest.py", "r", encoding="u8") as fp:
    exec(fp.read())

for number, images_ in images.items():
    for image in images_:
        src = f"img/{image}.jpg"
        dst = f"img-{number}/{image}.jpg"
        if os.path.exists(dst):
            print("文件存在", dst)
        else:
            print("复制文件", src, dst)
            shutil.copyfile(src, dst)

print("删除img目录")
shutil.rmtree("img", ignore_errors=True)

time2 = time.time()
sec = time2 - time1

print("创建write.png")
Image.new("RGB", (28, 28)).save("write.png")

print("安装依赖包")
pip.main(["install", "watchfiles"])

print()
print("成功，用时", sec, "秒 (", sec / 60, "分钟)")

if sec < 30:
    print("纪狗，qswl！")
elif sec < 120:
    print("你的速度超过了114514%的电脑")
elif sec < 450:
    print("这是正常速度")
else:
    print("这边建议换个硬盘")
