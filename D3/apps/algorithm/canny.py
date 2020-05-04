# @Description: canny.py
# @Author: 孤烟逐云zjy
# @Date: 2020/5/2 8:52
# @SoftWare: PyCharm
# @CSDN: https://blog.csdn.net/zjy123078_zjy
# @博客园: https://www.cnblogs.com/guyan-2020/


import cv2 as cv
import numpy as np
import urllib.request as urllib


def canny_imread(url):
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    # cv.imwrite("canny.jpg", cv.Canny(image, 200, 300))

    dst_img = cv.Canny(image, 200, 300)
    return dst_img

