# -*- coding: utf-8 -*-
from config import Config
from PIL import Image
import os


def check_image_type(perfix):
    '''
    校验图片类型
    :param perfix:
    :return:
    '''
    return perfix in Config.IMAGE_TYPE

def image_thumbnail(path, prefix, width=100, height=100):
    '''
    图片的缩率
    :param path:
    :param prefix:
    :param width:
    :param height:
    :return:
    '''
    img = Image.open(path)
    img.thumbnail((width, height))
    path_tmp = os.path.split(path)
    print("路径：",path)
    path = os.path.join(path_tmp[0], prefix+path_tmp[1])
    img.save(path)