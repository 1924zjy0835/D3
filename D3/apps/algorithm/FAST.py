# @Description: FAST.py
# @Author: 孤烟逐云zjy
# @Date: 2020/5/3 11:28
# @SoftWare: PyCharm
# @CSDN: https://blog.csdn.net/zjy123078_zjy
# @博客园: https://www.cnblogs.com/guyan-2020/

import numpy as np
import cv2 as cv
import urllib.request as urllib

# url = 'http://127.0.0.1:8088/media/photo01.min.jpg'


def fast(img_url):
    resp = urllib.urlopen(img_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv.imdecode(image, cv.IMREAD_COLOR)
# Initiate FAST object with default values
    fast = cv.FastFeatureDetector()
    # find and draw the keypoints
    kp = fast.detect(img,None)
    img2 = cv.drawKeypoints(img, kp, color=(255,0,0))
    # Print all default params
    print("Threshold: ", fast.getInt('threshold'))
    print("nonmaxSuppression: ", fast.getBool('nonmaxSuppression'))
    print("neighborhood: ", fast.getInt('type'))
    print("Total Keypoints with nonmaxSuppression: ", len(kp))
    # cv.imwrite('./images/fast_true.png',img2)
    # Disable nonmaxSuppression
    fast.setBool('nonmaxSuppression',0)
    kp = fast.detect(img,None)
    print("Total Keypoints without nonmaxSuppression: ", len(kp))
    img3 = cv.drawKeypoints(img, kp, color=(255,0,0))
    # cv.imwrite('./images/fast_false.png',img3)
    return img3


# fast(url)
# cv.waitKey(0)
# cv.destroyAllWindows()