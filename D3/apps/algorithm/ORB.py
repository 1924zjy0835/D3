# @Description: ORB.py
# @Author: 孤烟逐云zjy
# @Date: 2020/5/3 18:36
# @SoftWare: PyCharm
# @CSDN: https://blog.csdn.net/zjy123078_zjy
# @博客园: https://www.cnblogs.com/guyan-2020/


import cv2 as cv
import urllib.request as urllib
import numpy as np

# img = cv2.imread('./images/photo01.jpg', 0)


def orb(img_url):
    resp = urllib.urlopen(img_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv.imdecode(image, cv.IMREAD_COLOR)
    # Initiate STAR detector
    orb = cv.ORB_create()

    # find the keypoints with ORB
    kp = orb.detect(img,None)

    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)
    # kp, des = orb.detectAndCompute(img, None)

    # draw only keypoints location,not size and orientation
    img = cv.drawKeypoints(img,kp, None, color=(0,255,0), flags=0)
    return img

# plt.imshow(img),plt.show()