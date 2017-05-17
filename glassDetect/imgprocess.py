# -*-coding:utf-8 -*-
import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
import pylab as pl
from pprint import pprint

from logger import logger


def loadImage(img):
    try:
        srcImg = cv2.imread(img, 1)
        return srcImg
    except:
        logger.error("load image failed!")
        return None


def convertBGR2RGB(BGRImg):
    # b, g, r = cv2.split(BGRImg)
    # rgb_img = cv2.merge((r, g, b))
    RGBImg = cv2.cvtColor(BGRImg, cv2.COLOR_BGR2RGB)
    return RGBImg
    # return rgb_img


def resizeImage(img):
    res = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    return res


# 图像预处理,包括加载,转灰度图,二值化,返回二值化图像和阈值
def image_preprocess(srcImg):
    gray = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return (ret, thresh)


# 统计每行像素个数
def statistic_pixel_in_row(thresh_img):
    if len(thresh_img.shape) > 2:
        print("you should input a color image, not gray!")
        return
    pixels_in_row = []
    for row in range(thresh_img.shape[0]):
        pixel_count = 0
        for col in range(thresh_img.shape[1]):
            if thresh_img[row, col] > 0:
                pixel_count += 1
        pixels_in_row.append(pixel_count)
    # 返回行数和每行像素个数的列表
    return (thresh_img.shape[0], pixels_in_row)


def image_process(image_path):
    ret, thresh = image_preprocess(image_path)
    data = statistic_pixel_in_row(thresh)
    return data


def data_analysis(data):
    max_val = np.max(data[1])
    min_val = np.min(data[1])
    error_val = max_val - min_val
    return max_val, min_val, error_val


def main():
    image_path_list = get_images()
    data_list = []
    for image_path in image_path_list:
        data = image_process(image_path)
        data_list.append(data)
        data_analysised = data_analysis(data)
        print("max={}, min={}, error={}".format(data_analysised[0], data_analysised[1], data_analysised[2]))
        pl.plot([row for row in range(data[0])], data[1])
    # 在同一张图片上显示所有曲线
    pl.show()


# main()
