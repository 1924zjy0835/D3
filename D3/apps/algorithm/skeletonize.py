# @Description: skeletonize.py
# @Author: 孤烟逐云zjy
# @Date: 2020/5/3 8:30
# @SoftWare: PyCharm
# @CSDN: https://blog.csdn.net/zjy123078_zjy
# @博客园: https://www.cnblogs.com/guyan-2020/

import cv2 as cv
import numpy as np
import urllib.request as urllib


# 提取图像
# 对人体建模
# 使用OpenCV库计算生态骨架（morphological  skeleton）

def read_image(url):
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    dst_image = cv.imdecode(image, cv.IMREAD_GRAYSCALE)

    # 高斯模糊处理
    blur = cv.GaussianBlur(dst_image, (5,5), 0)
    # 二值化：Otsu's 二值化
    thresh, im = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    im = 255 - im
    # cv.imshow('binary.jpg', im)  # 控制背景为黑色
    dst = im.copy()

    num_erode = 0

    while (True):
        if np.sum(dst) == 0:
            break
        # getStructuringElement(内核的形状, 内核的尺寸, 锚点的位置):
        # MORPH_RECT：矩形；MORPH_CROSS：交叉形；MORPH_ELLIPSE：椭圆形；
        # 锚点的位置默认为（-1， -1），只是影响形态学运算结果的偏移
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        # kernel = cv.getStructuringElement(cv.MORPH_CROSS, (5, 5))
        dst = cv.erode(dst, kernel)
        num_erode = num_erode + 1

    skeleton = np.zeros(dst.shape, np.uint8)

    for x in range(num_erode):
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        # kernel = cv.getStructuringElement(cv.MORPH_CROSS, (5, 5))

        # erode(src, kernel, dst=None, anchor=None, iterations=None, borderType=None, borderValue=None):
        # 图像腐蚀，加上高斯模糊iterations=x，值越高，模糊程度越高，呈正相关；
        # 使得色彩追踪更加精准，少了很多颜色的干扰
        dst = cv.erode(im, kernel, None, None, x)
        # cv2.morphologyEx() :cv.MORPH_OPEN：进行开运算，先进行腐蚀，再进行膨胀；
        open_dst = cv.morphologyEx(dst, cv.MORPH_OPEN, kernel)
        # 求取腐蚀运算与开运算的差
        result = dst - open_dst
        # res = cv.bitwise_and(skeleton, result)
        skeleton = skeleton + result
        # cv.waitKey(10)

    return skeleton


