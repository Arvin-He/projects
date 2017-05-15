#! user/bin/python3
# -*- coding:utf-8 -*-

import os
from pprint import pprint
import numpy as np
import cv2
from matplotlib import pyplot as plt
import pylab as pl

image_path = os.path.abspath("res/image")

# 加载图像
def loadImage(image_path):
    image_list = []
    for img in os.listdir(image_path):
        if img.endswith(".bmp") or img.endswith(".png"):
            image_list.append(os.path.join(image_path, img))
    return image_list

# pprint(loadImage(image_path))

image_list = loadImage(image_path)

# 图像预处理,包括加载,转灰度图,二值化,返回二值化图像
def image_preprocess(image_path):
    print("image_path={}".format(image_path))
    try:
        srcImg = cv2.imread(image_path, 1)
        gray = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)
    except:
        print("Load image failed!")
        return None
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    print("thresh value = {}".format(ret))
    plt.imshow(thresh, cmap='gray', interpolation='bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()
    return (ret, thresh)

def splitBolt(img):
    pass

def colorDetect(img):
    pass



image_preprocess(image_list[0])
image_preprocess(image_list[1])
image_preprocess(image_list[2])
image_preprocess(image_list[3])