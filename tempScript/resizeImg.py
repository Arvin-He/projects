#!usr/bin/python3
# -*- coding:utf-8 -*-
import os
import cv2


def output_image_info(img):
    print("-----------------------------------------------------------")
    if len(img.shape) == 2:
        print("image size = {} X {}".format(img.shape[0], img.shape[1]))
        print("image channels = 1")
    else:
        print("image size = {} X {}".format(img.shape[0], img.shape[1]))
        print("image channels = {}".format(img.shape[2]))
    print("-----------------------------------------------------------")


def load_image(img):
    try:
        srcImg = cv2.imread(os.path.abspath(img), 0)
        output_image_info(srcImg)
        return srcImg
    except:
        print("load image failed!")
        return None


def resize_image(img):
    dst = cv2.resize(img, (640, 640), interpolation=cv2.INTER_CUBIC)
    # 裁剪
    dst = dst[80:560, 0:640]
    return dst


def save_image(dst_path, img):
    cv2.imwrite(dst_path, img)


input_path = "./GFD"
for dirpath, dirnames, filenames in os.walk(input_path):
    for f in filenames:
        if f.endswith(".BMP"):
            fullname = os.path.join(dirpath, f)
            src = load_image(fullname)
            if src is not None:
                dst_path = dirpath + "_2"
                if not os.path.exists(dst_path):
                    os.mkdir(dst_path)

            dst = resize_image(src)
            dst_name = os.path.join(dst_path, f)
            save_image(dst_name, dst)



