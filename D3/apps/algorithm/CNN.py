# @Description: CNN.py
# @Author: 孤烟逐云zjy
# @Date: 2020/5/1 10:47
# @SoftWare: PyCharm
# @CSDN: https://blog.csdn.net/zjy123078_zjy
# @博客园: https://www.cnblogs.com/guyan-2020/

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

import urllib.request as urllib


def imread_image(url):
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    return image


def normal(image, kernel):
    res = np.multiply(image, kernel).sum()

    if res > 255:
        return 255
    elif res < 0:
        return 0
    else:
        return res


def _convolve(image, kernel):
    h_kernel, w_kernel = kernel.shape
    h_image, w_image = image.shape

    res_h = h_image - h_kernel + 1
    res_w = w_image - w_kernel + 1

    res = np.zeros((res_h, res_w),np.uint8)
    for i in range(res_h):
        for j in range(res_w):
            res[i, j] = normal(image[i:i + h_kernel, j:j + w_kernel], kernel)

    return res


def conv(image, kernel, mode='same'):
    if mode == 'fill':
        h = kernel.shape[0]
        w = kernel.shape[1]

        image = np.pad(image, ((h, h), (w, w), (0, 0)), 'constant')
    conv_b = _convolve(image[:, :, 0], kernel)
    conv_g = _convolve(image[:, :, 1], kernel)
    conv_r = _convolve(image[:, :, 2], kernel)
    res = np.dstack([conv_b, conv_g, conv_r])
    return res


# if __name__ == '__main__':
    # 读取要处理的图像
    # path = './images/photo01.jpg'
    # url = "http://q87jey5py.bkt.clouddn.com/photo01.jpg"
    # image = cv.imread(path)
    # image = imread_image(url)

    # 自定义卷积核
    # kernel 是一个3*3的边缘特征提取器，可以提取各个方向上的边缘
    # kernel2 是一个5*5的浮雕特征提取器

    # kernel 之和为0、或小于0的时候，为黑色
    # kernel 之和大于0的时候为彩色
    # kernel = np.array([
    #     [1, 1, 1],
    #     [1, -8, 1],
    #     [1, 1, 1]
    # ])

    # res = conv(image, kernel, 'fill')
    # plt.imshow(res)
    # # 关闭图像的坐标轴
    # plt.axis('off')
    # plt.show()
