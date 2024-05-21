import os

import pygame as pg
import xlrd
from pygame.locals import *

pg.init()

def load_all_gfx(directory, colorkey=(0, 0, 0), accept=(".png", ".jpg", ".bmp")):
    '''
    将指定路径文件夹中的所有图片转换为pygame里的Surface，以字典形式存储
    如 image 文件夹下有 a.png,b.jpg 两个文件
    在通过 pic = load_all_gfx('image')后
    可以使用pic['a'],pic['b']分别代表图像图层使用，可以后续进行blit等操作
    :param directory: 文件路径
    :param colorkey: 如果有透明通道，此处为（0，0，0，0）
    :param accept: 可以接收的文件后缀名
    :return: 返回字典形式的pygame.Surface
    '''

    graphics = {}          #创建字典放置surface格式图片
    for pic in os.listdir(directory):    #通过循环遍历文件夹里的文件
        name, ext = os.path.splitext(pic)  #将文件名和后缀名分开
        if ext.lower() in accept:          #后缀名转换为小写后看是否为指定的图片文件格式
            img = pg.image.load(os.path.join(directory, pic))      #通过pygame里载入图片的方式把文件转为Surface
            # pg.image.save(img, os.path.join(directory, pic))
            if img.get_alpha():                          # 如图片中含有透明通道
                img = img.convert_alpha()                # 将图片转化为透明图层
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img                           # 通过循环将所有图片放入字典
    return graphics


def load_all_music(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    '''
    字典形式载入多个音乐文件，可以参考load_all_gfx函数
    :param directory: 文件路径
    :param accept: 可以接受的文件后缀名
    :return: 字典形式的歌曲文件
    '''

    songs = {}
    for song in os.listdir(directory):
        name, ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_fonts(directory, accept=(".ttf",)):
    '''
    字典形式载入多个字体文件，可以参考load_all_gfx函数
    :param directory: 文件路径
    :param accept: 可以接受的文件后缀名
    :return: 字典形式的字体文件
    '''
    return load_all_music(directory, accept)


def load_all_sfx(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    '''
    字典形式载入多个音效，可以参考load_all_gfx函数
    :param directory: 文件路径
    :param accept: 可接受的文件后缀名
    :return: 字典形式的字体文件
    '''
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects


def load_all_maps(directory, accept=(".xls")):
    '''
    字典形式载入多个地图文件
    :param directory:文件路径
    :param accept:可接受的文件后缀名
    :return:字典形式的地图
    '''
    game_maps = {}                   #创建空字典
    for game_map in os.listdir(directory):         #遍历路径里的所有文件
        name, ext = os.path.splitext(game_map)      #仅载入后缀为excel格式的文件
        if ext.lower() in accept:
             data = xlrd.open_workbook(os.path.join(directory, game_map))  #通过xlrd库载入excel为python
             game_maps[name] = data.sheet_by_index(0)                      #这里只用sheet1
    return game_maps


GFX = load_all_gfx(os.path.join("resources", "graphics"))  # 包括所有图片的字典
FONTS = load_all_fonts(os.path.join("resources", "fonts"))  # 包括所有字体的字典
SFX = load_all_sfx(os.path.join("resources", "sound"))  # 包括所有音效的字典
MUSIC = load_all_music(os.path.join("resources", "music"))  # 包括所有音乐的字典
HEXS = load_all_gfx(os.path.join("resources", "graphics", "Hex", "Hex"))  # 包括所有地图图元的字典
GAME_MAPS = load_all_maps(os.path.join("resources", "game_maps"))  # 包括所有地图的字典
PIECES = load_all_gfx(os.path.join("resources", "graphics", "piece"))
GRAPHICS = load_all_gfx(os.path.join("resources", "graphics"))
