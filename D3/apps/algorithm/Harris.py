# @Description: Harris.py
# @Author: 孤烟逐云zjy
# @Date: 2020/5/3 8:51
# @SoftWare: PyCharm
# @CSDN: https://blog.csdn.net/zjy123078_zjy
# @博客园: https://www.cnblogs.com/guyan-2020/


import cv2 as cv
import numpy as np


def Harris(image):
    gray = cv.Canny(image, 200, 300)
    # gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)

    dst = cv.cornerHarris(gray, 2, 3, 0.04)
    dst = cv.dilate(dst, None)

    image[dst > 0.01*dst.max()] = [0, 0, 255]
    cv.imshow('dst', gray)
    #
    # plt.imshow(image)
    # plt.show()

    # if cv.waitKey(0)&0xff == 27:
    #     cv.destroyAllWindows()
    return image