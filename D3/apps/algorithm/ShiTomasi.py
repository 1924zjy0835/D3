# @Description: ShiTomasi.py
# @Author: 孤烟逐云zjy
# @Date: 2020/5/3 8:52
# @SoftWare: PyCharm
# @CSDN: https://blog.csdn.net/zjy123078_zjy
# @博客园: https://www.cnblogs.com/guyan-2020/


import numpy as np
import cv2 as cv


def ShiTomasi(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # gray = cv.Canny(img, 200, 300)
    corners = cv.goodFeaturesToTrack(gray, 25, 0.01, 10)
    corners = np.int0(corners)

    for i in corners:
        x, y = i.ravel()
        cv.circle(image, (x, y),3, 255, -1)
    return image
