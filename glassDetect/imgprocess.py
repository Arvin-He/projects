# -*-coding:utf-8 -*-
import cv2
import numpy as np
from collections import Counter

from logger import logger

imageWidth = 500
imageHeight = 400


def loadImage(img):
    try:
        srcImg = cv2.imread(img, 1)
        return srcImg
    except:
        logger.error("load image failed!")
        return None


def convertBGR2RGB(BGRImg):
    RGBImg = cv2.cvtColor(BGRImg, cv2.COLOR_BGR2RGB)
    return RGBImg


def resizeImg(img):
    res = cv2.resize(
        img, (imageWidth, imageHeight), interpolation=cv2.INTER_CUBIC)
    return res


# 二值化, 返回二值化图像和阈值
def threshImg(img):
    if len(img.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    ret, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return (ret, thresh)


# 获取每行像素个数,返回由两个列表组成的元组
def getRowPixels(img):
    if len(img.shape) > 2:
        logger.error("please input a binary image, not color!")
        return
    pixels_list = []
    for row in range(img.shape[0]):
        pixel_count = 0
        for col in range(img.shape[1]):
            if img[row, col] > 0:
                pixel_count += 1
        pixels_list.append(pixel_count)
    return (img.shape[0], pixels_list)


def get_image_process_data(img):
    ret, thresh = threshImg(img)
    data = getRowPixels(thresh)
    return data


def data_analysis(data):
    if data:
        res = {}
        res["min"] = np.min(data[1])
        res["max"] = np.max(data[1])
        res["mean"] = np.mean(data[1])
        res["diff"] = res["max"] - res["min"]
        estimate_val = Counter(data[1])
        res["estimate"] = estimate_val.most_common(1)[0][0]
        return res
