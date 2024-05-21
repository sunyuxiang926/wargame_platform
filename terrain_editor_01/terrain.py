import pygame as pg

from resources.load_data import HEXS, GAME_MAPS
from platform_settings_07.control_class import font_surface


# 以下编码中含有硬编码，为六角格瓦片地图的尺寸大小
# 六角格瓦片地图长 54 高 60 中心垂直距离 45
# 六角格上下堆叠 中心垂直距离 45 = 60 /4 * 3
# ---------------定义六角格类，用于对地形六角格属性的描述、显示与编辑


def cube_to_oddr(x, y, z):
    '''
    将六角格坐标系的x,y,z坐标转换为row,col
    :param x:
    :param y:
    :param z:
    :return:
    '''
    col = x + (z - (z & 1)) / 2
    row = z
    return (row, col)


def oddr_to_cube(row, col):
    '''
    将六角格坐标系的row,col坐标转换为x,y,z
    :param row:
    :param col:
    :return:
    '''
    x = col - (row - (row & 1)) / 2
    z = row
    y = -x - z
    return (x, y, z)


class Hexagon(pg.sprite.Sprite):
    def __init__(self, hexagon_id, m_coordinate, m_elevation, m_landform, m_position):  # m_coordinate坐标
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images\hex.png").convert_alpha()
        self.active = False  # 标识是否选中六角格
        self.Edited = False  # 标识是否编辑
        self.mask = pg.mask.from_surface(self.image)  # 返回非透明部分的掩码值
        self.pre_hex_surf = self.image  # 用于随地图移动缩放的前对象
        self.pos_hex_surf = self.pre_hex_surf  # 用于随地图移动缩放的后对象
        self.pre_hex_rect = self.pre_hex_surf.get_rect()
        self.pos_hex_rect = self.pos_hex_surf.get_rect()
        # -----六角格的描述模型，数据结构------
        self.pre_hex_rect.topleft = m_position
        self.pos_hex_rect.topleft = m_position
        self.ID = hexagon_id
        self.coordinate = m_coordinate
        self.elevation = m_elevation
        self.landform = m_landform


class Game_map(object):
    offline_potiential = {(1, 17): 8, (1, 20): 2, (1, 21): 3, (1, 22): 3, (1, 23): 5, (1, 25): 6, (1, 26): 5,
                          (1, 28): 4,
                          (1, 29): 7, (1, 30): 22, (1, 31): 1, (1, 36): 2, (1, 40): 2, (3, 14): 1, (2, 15): 2,
                          (2, 17): 1,
                          (3, 17): 3, (2, 18): 6, (2, 19): 5, (3, 19): 5, (3, 20): 1, (2, 21): 6, (3, 21): 6,
                          (2, 22): 23,
                          (3, 22): 38, (2, 23): 26, (3, 23): 62, (2, 24): 17, (3, 24): 39, (2, 25): 10, (3, 25): 2,
                          (2, 26): 3, (3, 26): 3, (3, 27): 32, (3, 28): 9, (2, 29): 2, (3, 29): 28, (2, 30): 1,
                          (3, 30): 10,
                          (2, 31): 11, (3, 31): 16, (2, 32): 2, (3, 32): 1, (3, 37): 2, (2, 38): 2, (3, 38): 2,
                          (5, 7): 2,
                          (5, 13): 6, (5, 15): 3, (5, 17): 3, (5, 18): 10, (4, 19): 4, (5, 19): 8, (4, 20): 4,
                          (5, 20): 27,
                          (4, 21): 14, (5, 21): 1, (5, 22): 2, (4, 23): 9, (5, 23): 7, (4, 24): 22, (5, 24): 3,
                          (4, 25): 4,
                          (5, 25): 3, (5, 26): 12, (4, 27): 21, (5, 27): 208, (4, 28): 15, (5, 28): 124, (4, 29): 5,
                          (5, 29): 23, (4, 30): 1, (5, 30): 24, (5, 31): 24, (4, 32): 5, (5, 32): 25, (4, 33): 27,
                          (5, 33): 12, (4, 34): 3, (5, 34): 10, (4, 35): 6, (5, 35): 2, (4, 36): 11, (5, 36): 19,
                          (4, 37): 34, (5, 37): 14, (7, 9): 4, (6, 10): 1, (6, 11): 2, (6, 12): 16, (6, 13): 17,
                          (6, 14): 8,
                          (7, 14): 1, (6, 15): 3, (6, 16): 3, (7, 16): 5, (6, 17): 29, (7, 17): 18, (6, 18): 4,
                          (7, 18): 38,
                          (6, 19): 9, (7, 19): 117, (7, 20): 19, (6, 21): 6, (7, 21): 27, (6, 22): 139, (7, 22): 7,
                          (6, 23): 73, (7, 23): 12, (6, 24): 195, (7, 24): 132, (6, 25): 42, (7, 25): 21, (6, 26): 36,
                          (7, 26): 32, (6, 27): 89, (7, 27): 19, (6, 28): 88, (7, 28): 140, (6, 29): 379, (7, 29): 54,
                          (6, 30): 41, (7, 30): 26, (6, 31): 12, (7, 31): 17, (6, 32): 13, (6, 33): 4, (6, 34): 3,
                          (6, 39): 1, (9, 10): 3, (8, 13): 1, (8, 15): 7, (9, 15): 6, (8, 16): 21, (9, 16): 2,
                          (8, 17): 32,
                          (9, 17): 55, (8, 18): 27, (9, 18): 81, (8, 19): 76, (9, 19): 12, (8, 20): 30, (9, 20): 39,
                          (8, 21): 17, (9, 21): 11, (8, 22): 48, (9, 22): 8, (8, 23): 54, (9, 23): 49, (8, 24): 306,
                          (9, 24): 13, (8, 25): 19, (9, 25): 1, (8, 26): 16, (9, 26): 2, (8, 27): 22, (9, 27): 33,
                          (8, 28): 88, (9, 28): 63, (8, 29): 61, (9, 29): 24, (8, 30): 10, (9, 30): 51, (8, 31): 38,
                          (8, 33): 3, (9, 33): 2, (8, 35): 1, (9, 39): 3, (11, 11): 13, (10, 12): 2, (11, 12): 6,
                          (10, 13): 8, (11, 13): 1, (10, 14): 5, (11, 14): 10, (10, 15): 1, (11, 15): 10, (10, 16): 20,
                          (11, 16): 11, (10, 17): 113, (11, 17): 18, (10, 18): 483, (11, 18): 4, (10, 19): 75,
                          (11, 19): 7,
                          (10, 20): 13, (11, 20): 15, (10, 21): 20, (11, 21): 5, (10, 22): 8, (11, 22): 1, (10, 23): 6,
                          (11, 23): 8, (10, 24): 21, (11, 24): 15, (10, 25): 5, (11, 25): 10, (10, 26): 13,
                          (11, 26): 164,
                          (10, 27): 36, (11, 27): 203, (10, 28): 180, (11, 28): 182, (10, 29): 50, (11, 29): 9,
                          (10, 30): 52, (11, 30): 6, (10, 31): 1, (11, 31): 1, (11, 32): 12, (11, 35): 1, (11, 36): 2,
                          (11, 37): 1, (10, 39): 4, (11, 40): 64, (10, 42): 3, (11, 42): 4, (10, 43): 4, (11, 43): 3,
                          (13, 8): 2, (12, 9): 5, (12, 10): 1, (13, 10): 3, (12, 11): 7, (13, 12): 3, (12, 13): 1,
                          (13, 13): 3, (12, 14): 2, (13, 14): 169, (12, 15): 3, (13, 15): 8, (12, 16): 19, (13, 16): 8,
                          (12, 17): 3, (13, 17): 3, (12, 18): 11, (13, 18): 6, (12, 19): 10, (13, 19): 42, (12, 20): 15,
                          (13, 20): 25, (12, 21): 14, (13, 21): 21, (13, 22): 12, (12, 23): 5, (13, 23): 26,
                          (12, 24): 28,
                          (13, 24): 42, (12, 25): 10, (13, 25): 136, (12, 26): 11, (13, 26): 287, (12, 27): 67,
                          (13, 27): 155, (12, 28): 71, (13, 28): 161, (12, 29): 81, (13, 29): 5, (12, 30): 62,
                          (13, 30): 145, (13, 31): 3, (12, 32): 1, (13, 32): 4, (13, 33): 4, (12, 34): 1, (12, 35): 1,
                          (13, 35): 45, (12, 36): 6, (13, 36): 10, (12, 37): 5, (13, 37): 9, (12, 39): 1, (13, 39): 8,
                          (12, 40): 3, (13, 41): 5, (13, 43): 1, (12, 44): 2, (13, 45): 7, (13, 47): 3, (15, 7): 8,
                          (14, 8): 1, (14, 10): 1, (14, 12): 1, (14, 13): 7, (15, 13): 18, (14, 14): 96, (15, 14): 377,
                          (14, 15): 1, (15, 15): 4, (14, 16): 9, (14, 17): 15, (15, 17): 23, (14, 18): 34, (15, 18): 24,
                          (14, 19): 57, (15, 19): 64, (14, 20): 80, (15, 20): 411, (14, 21): 66, (15, 21): 129,
                          (14, 22): 29, (15, 22): 186, (14, 23): 68, (15, 23): 366, (14, 24): 76, (15, 24): 465,
                          (14, 25): 90, (15, 25): 193, (14, 26): 108, (15, 26): 303, (14, 27): 54, (15, 27): 83,
                          (14, 28): 81, (15, 28): 125, (14, 29): 97, (15, 29): 6, (14, 30): 99, (15, 30): 8,
                          (14, 31): 5,
                          (15, 31): 12, (14, 32): 2, (14, 33): 5, (15, 34): 4, (14, 35): 17, (14, 36): 7, (14, 37): 3,
                          (14, 38): 2, (14, 39): 12, (15, 39): 5, (14, 40): 2, (15, 40): 5, (14, 41): 1, (15, 41): 1,
                          (14, 43): 2, (15, 43): 5, (14, 45): 2, (15, 45): 6, (14, 47): 7, (15, 48): 14, (17, 3): 6,
                          (17, 4): 1, (17, 5): 17, (17, 6): 3, (17, 8): 13, (17, 9): 37, (17, 10): 1, (16, 11): 1,
                          (17, 11): 2, (17, 12): 76, (16, 13): 15, (17, 13): 24, (16, 14): 1, (17, 14): 6, (16, 16): 4,
                          (17, 16): 7, (16, 17): 4, (17, 17): 2, (16, 18): 29, (17, 18): 31, (16, 19): 628,
                          (17, 19): 490,
                          (16, 20): 160, (17, 20): 73, (16, 21): 215, (17, 21): 159, (16, 22): 344, (17, 22): 314,
                          (16, 23): 789, (17, 23): 1643, (16, 24): 4515, (17, 24): 2662, (16, 25): 1118, (17, 25): 962,
                          (16, 26): 156, (17, 26): 210, (16, 27): 117, (17, 27): 139, (16, 28): 75, (17, 28): 105,
                          (16, 29): 65, (17, 29): 82, (16, 30): 7, (17, 30): 15, (16, 31): 5, (16, 32): 7, (17, 32): 4,
                          (16, 33): 1, (16, 34): 20, (17, 34): 45, (16, 35): 7, (17, 35): 8, (16, 36): 938, (17, 36): 3,
                          (17, 37): 14, (16, 38): 2, (17, 38): 2, (16, 39): 5, (17, 39): 5, (16, 40): 6, (17, 40): 6,
                          (16, 41): 1, (17, 41): 5, (17, 42): 2, (17, 43): 1, (17, 44): 9, (16, 45): 5, (16, 46): 1,
                          (17, 46): 1, (16, 47): 3, (17, 47): 1, (16, 48): 12, (17, 48): 13, (16, 49): 10, (16, 50): 3,
                          (19, 0): 1, (18, 1): 4, (19, 1): 1, (18, 2): 3, (19, 2): 9, (18, 3): 3, (19, 3): 6,
                          (18, 4): 9,
                          (19, 4): 9, (18, 5): 9, (19, 5): 11, (18, 6): 9, (19, 6): 1, (18, 8): 7, (19, 8): 15,
                          (18, 9): 19,
                          (18, 10): 1, (19, 10): 10, (18, 11): 3, (19, 11): 60, (18, 12): 3, (19, 12): 17, (18, 13): 1,
                          (19, 13): 4, (18, 14): 5, (19, 14): 24, (18, 15): 3, (19, 15): 22, (18, 16): 3, (19, 16): 21,
                          (18, 17): 14, (19, 17): 26, (18, 18): 19, (19, 18): 24, (18, 19): 51, (19, 19): 136,
                          (18, 20): 412, (19, 20): 98, (18, 21): 104, (19, 21): 188, (18, 22): 302, (19, 22): 601,
                          (18, 23): 391, (19, 23): 423, (18, 24): 582, (19, 24): 678, (18, 25): 2682, (19, 25): 1241,
                          (18, 26): 586, (19, 26): 206, (18, 27): 191, (19, 27): 64, (18, 28): 86, (19, 28): 375,
                          (18, 29): 282, (19, 29): 21, (18, 30): 17, (19, 30): 4, (18, 31): 2, (19, 31): 20,
                          (18, 32): 5,
                          (19, 32): 15, (18, 33): 12, (19, 33): 6, (18, 34): 19, (19, 34): 15, (18, 35): 44,
                          (19, 35): 100,
                          (18, 36): 35, (19, 36): 1, (18, 37): 6, (19, 37): 3, (18, 38): 18, (19, 38): 1, (18, 39): 2,
                          (18, 40): 11, (18, 41): 4, (18, 42): 5, (18, 43): 1, (18, 44): 2, (19, 45): 1, (18, 46): 5,
                          (19, 46): 1, (18, 47): 2, (19, 47): 3, (18, 50): 3, (18, 51): 3, (18, 52): 2, (19, 52): 1,
                          (21, 0): 2, (21, 1): 2, (20, 3): 1, (21, 3): 2, (20, 4): 6, (21, 4): 2, (20, 5): 6,
                          (21, 5): 4,
                          (20, 6): 4, (20, 7): 8, (20, 8): 1, (20, 11): 5, (20, 12): 259, (21, 12): 235, (20, 13): 7,
                          (21, 13): 4, (20, 14): 6, (21, 14): 10, (20, 15): 18, (21, 15): 25, (20, 16): 9, (21, 16): 15,
                          (20, 17): 6, (21, 17): 13, (20, 18): 9, (21, 18): 22, (20, 19): 36, (21, 19): 30,
                          (20, 20): 128,
                          (21, 20): 122, (20, 21): 121, (21, 21): 88, (20, 22): 195, (21, 22): 155, (20, 23): 377,
                          (21, 23): 598, (20, 24): 536, (21, 24): 2962, (20, 25): 1041, (21, 25): 642, (20, 26): 534,
                          (21, 26): 560, (20, 27): 577, (21, 27): 44, (20, 28): 398, (21, 28): 18, (20, 29): 23,
                          (21, 29): 16, (20, 30): 7, (21, 30): 9, (20, 31): 1, (21, 31): 3, (20, 32): 9, (21, 32): 16,
                          (20, 33): 13, (21, 33): 14, (20, 34): 10, (21, 34): 14, (20, 35): 162, (21, 35): 11,
                          (20, 36): 1,
                          (21, 36): 19, (21, 37): 7, (21, 38): 2, (20, 39): 14, (21, 39): 7, (20, 41): 5, (20, 42): 2,
                          (21, 44): 1, (20, 45): 7, (20, 46): 5, (20, 51): 1, (20, 52): 1, (20, 53): 2, (22, 3): 7,
                          (23, 4): 3, (23, 5): 2, (23, 6): 2, (22, 7): 7, (23, 7): 5, (23, 8): 1, (22, 9): 1,
                          (23, 9): 5,
                          (22, 10): 2, (23, 10): 4, (22, 11): 3, (23, 11): 3, (22, 12): 2, (23, 12): 3, (23, 13): 11,
                          (22, 14): 12, (23, 14): 8, (22, 15): 8, (23, 15): 87, (22, 16): 4, (23, 16): 19,
                          (22, 17): 104,
                          (23, 17): 28, (22, 18): 30, (23, 18): 26, (22, 19): 23, (23, 19): 53, (22, 20): 230,
                          (23, 20): 46,
                          (22, 21): 58, (23, 21): 179, (22, 22): 81, (23, 22): 262, (22, 23): 264, (23, 23): 335,
                          (22, 24): 1207, (23, 24): 175, (22, 25): 541, (23, 25): 198, (22, 26): 164, (23, 26): 231,
                          (22, 27): 271, (23, 27): 363, (22, 28): 20, (23, 28): 22, (22, 29): 7, (23, 29): 8,
                          (22, 30): 1,
                          (23, 30): 3, (22, 31): 1, (23, 31): 3, (22, 32): 5, (23, 32): 6, (23, 33): 8, (22, 34): 3,
                          (23, 34): 5, (23, 35): 4, (22, 36): 4, (23, 36): 3, (22, 37): 2, (23, 38): 3, (23, 39): 26,
                          (22, 44): 3, (23, 44): 6, (22, 46): 1, (23, 49): 3, (24, 1): 1, (24, 4): 2, (24, 6): 1,
                          (25, 6): 1, (24, 7): 3, (24, 8): 14, (24, 9): 3, (24, 10): 4, (25, 10): 2, (24, 11): 7,
                          (25, 11): 5, (24, 12): 7, (25, 12): 1, (24, 13): 2, (25, 13): 12, (24, 14): 3, (25, 14): 5,
                          (24, 15): 22, (25, 15): 6, (24, 16): 8, (25, 16): 8, (24, 17): 9, (25, 17): 12, (24, 18): 11,
                          (25, 18): 39, (24, 19): 19, (25, 19): 37, (24, 20): 24, (25, 20): 92, (24, 21): 23,
                          (25, 21): 37,
                          (24, 22): 28, (25, 22): 29, (24, 23): 147, (25, 23): 28, (24, 24): 30, (25, 24): 47,
                          (24, 25): 64,
                          (25, 25): 93, (24, 26): 139, (25, 26): 164, (24, 27): 192, (25, 27): 34, (24, 28): 19,
                          (25, 28): 346, (24, 29): 11, (25, 29): 16, (24, 30): 5, (25, 30): 5, (24, 31): 3, (25, 32): 4,
                          (25, 33): 1, (24, 34): 3, (25, 34): 2, (25, 35): 4, (25, 36): 8, (24, 37): 2, (25, 37): 4,
                          (24, 38): 1, (25, 38): 3, (24, 39): 9, (25, 39): 4, (24, 40): 1, (25, 40): 11, (24, 41): 6,
                          (25, 44): 2, (25, 45): 2, (25, 51): 1, (26, 5): 2, (26, 7): 3, (26, 12): 5, (27, 12): 2,
                          (27, 13): 2, (27, 14): 1, (26, 15): 5, (27, 15): 8, (26, 16): 12, (26, 17): 11, (27, 17): 47,
                          (26, 18): 16, (27, 18): 6, (26, 19): 1, (27, 19): 29, (26, 20): 531, (27, 20): 166,
                          (26, 21): 18,
                          (27, 21): 16, (26, 22): 14, (27, 22): 20, (26, 23): 9, (27, 23): 15, (26, 24): 29,
                          (27, 24): 33,
                          (26, 25): 74, (27, 25): 106, (26, 26): 99, (27, 26): 132, (26, 27): 209, (27, 27): 16,
                          (26, 28): 18, (27, 28): 5, (26, 29): 9, (26, 30): 5, (27, 30): 3, (27, 31): 1, (26, 32): 2,
                          (27, 32): 7, (26, 33): 9, (27, 33): 1, (26, 35): 94, (27, 35): 10, (27, 37): 1, (26, 42): 3,
                          (27, 43): 1, (27, 49): 2, (28, 12): 11, (28, 13): 10, (28, 14): 12, (29, 14): 3, (29, 15): 17,
                          (28, 16): 23, (29, 16): 6, (28, 17): 6, (29, 17): 4, (28, 18): 31, (29, 18): 42, (28, 19): 58,
                          (29, 19): 26, (28, 20): 11, (29, 20): 50, (28, 21): 221, (29, 21): 123, (28, 22): 45,
                          (29, 22): 53, (28, 23): 8, (29, 23): 24, (28, 24): 16, (29, 24): 94, (28, 25): 44,
                          (29, 25): 183,
                          (28, 26): 202, (29, 26): 32, (28, 27): 241, (29, 27): 8, (28, 28): 274, (29, 28): 33,
                          (28, 29): 22, (29, 29): 329, (28, 30): 5, (29, 30): 30, (28, 31): 1, (29, 31): 14,
                          (28, 32): 11,
                          (29, 32): 6, (28, 33): 8, (28, 34): 9, (29, 34): 5, (28, 35): 9, (28, 36): 60, (29, 36): 11,
                          (29, 37): 11, (28, 38): 5, (29, 38): 1, (29, 39): 1, (28, 40): 2, (29, 40): 1, (28, 42): 1,
                          (29, 42): 5, (28, 43): 12, (28, 44): 1, (29, 44): 1, (31, 14): 4, (30, 16): 2, (31, 17): 1,
                          (30, 18): 1, (30, 19): 23, (31, 19): 7, (30, 20): 10, (31, 20): 5, (30, 21): 11,
                          (31, 21): 105,
                          (30, 22): 116, (31, 22): 64, (30, 23): 106, (31, 23): 9, (30, 24): 161, (31, 24): 9,
                          (30, 25): 12,
                          (31, 25): 13, (30, 26): 15, (31, 27): 2, (30, 28): 3, (30, 29): 1, (31, 29): 2, (30, 30): 3,
                          (31, 30): 5, (30, 31): 35, (31, 31): 17, (31, 32): 4, (30, 33): 9, (31, 34): 1, (30, 35): 3,
                          (31, 35): 1, (30, 36): 1, (31, 36): 1, (31, 37): 2, (31, 39): 2, (30, 40): 4, (30, 51): 1,
                          (33, 15): 5, (32, 16): 3, (33, 16): 3, (32, 17): 4, (33, 17): 51, (33, 18): 3, (32, 19): 5,
                          (33, 19): 9, (32, 20): 12, (33, 20): 3, (32, 21): 7, (33, 21): 5, (32, 22): 67, (33, 22): 22,
                          (33, 23): 5, (32, 24): 2, (32, 26): 5, (33, 26): 1, (32, 28): 5, (33, 29): 2, (33, 30): 53,
                          (32, 31): 8, (32, 32): 2, (33, 32): 3, (32, 33): 3, (32, 35): 1, (32, 36): 4, (33, 36): 1,
                          (32, 37): 2, (32, 38): 2, (33, 40): 1, (33, 42): 2, (33, 43): 3, (34, 11): 1, (34, 15): 2,
                          (35, 15): 7, (35, 16): 4, (34, 17): 2, (35, 17): 1, (34, 18): 10, (34, 19): 1, (35, 19): 4,
                          (34, 20): 6, (34, 22): 30, (34, 23): 7, (34, 24): 2, (35, 24): 3, (35, 27): 3, (35, 29): 3,
                          (34, 30): 1, (35, 30): 3, (34, 31): 5, (35, 31): 4, (34, 32): 4, (35, 32): 4, (35, 36): 1,
                          (34, 38): 2, (34, 40): 2, (35, 40): 1, (36, 14): 9, (36, 15): 4, (36, 16): 3, (37, 17): 65,
                          (36, 18): 4, (37, 18): 60, (37, 19): 4, (36, 20): 2, (37, 21): 1, (36, 22): 1, (36, 23): 4,
                          (37, 23): 15, (36, 24): 2, (37, 24): 1, (36, 25): 3, (37, 29): 4, (36, 30): 9, (37, 30): 5,
                          (36, 31): 3, (36, 32): 3, (37, 32): 2, (37, 33): 1, (36, 41): 2, (39, 15): 1, (39, 16): 4,
                          (38, 17): 1, (39, 17): 2, (38, 18): 17, (39, 18): 68, (38, 19): 5, (39, 19): 1, (38, 20): 10,
                          (39, 20): 6, (38, 23): 5, (38, 24): 4, (38, 25): 4, (38, 26): 3, (38, 29): 1, (39, 31): 5,
                          (39, 32): 2, (38, 33): 16, (39, 33): 2, (38, 34): 2, (39, 34): 1, (39, 36): 1, (38, 37): 1,
                          (38, 39): 1, (41, 15): 1, (41, 16): 2, (40, 17): 4, (40, 18): 1, (41, 18): 4, (40, 19): 4,
                          (41, 23): 2, (40, 24): 1, (41, 24): 5, (41, 26): 3, (41, 27): 1, (41, 28): 1, (40, 29): 2,
                          (42, 17): 2, (43, 18): 1, (42, 21): 1, (42, 27): 2, (42, 28): 1, (42, 41): 3, (45, 11): 1,
                          (44, 12): 2, (44, 15): 1, (45, 15): 1, (44, 19): 3, (46, 9): 1, (47, 10): 3, (47, 19): 1,
                          (46, 21): 2, (48, 13): 1, (48, 18): 1, (48, 20): 2, (48, 21): 2}
    def __init__(self, wargame):
        super(Game_map, self).__init__()
        self.wargame_env = wargame

        self.map_offset = [54 / 2 * 16 - 400, 60 / 2.0 * 15]  # 设置地图相对窗口坐标系的偏移量
        # '01城镇居民地', '02岛上台地', '03高原通道','05山岳丛林地','06水网稻田地'
        self.map_excel_data = GAME_MAPS['01城镇居民地']
        self.map_hex_pic = HEXS
        self.surface = self.load_terrianmap(self.map_hex_pic, self.map_excel_data)
        self.draw_line_init()  # 画线测量距离
        self.grab_map = False  # 鼠标点选移动地图

    def draw(self, surface):
        # 将地图绘制在屏幕上
        surface.blit(self.surface, (-self.map_offset[0], -self.map_offset[1]))
        if self.draw_line and self.measure_end_point != (0, 0):
            # 将测量距离的线画在地图上
            pg.draw.line(surface, (255, 0, 0), self.measure_start_point, self.measure_end_point)

    def draw_line_init(self):
        '''
        画线初始化，设置画线布尔值，画线起点，画线重点，画线距离，单位为六角格
        :return:
        '''
        self.draw_line = False
        self.measure_start_point = (0, 0)
        self.measure_end_point = (0, 0)
        self.measure_distance = 0

    # 按住上下左右键导览地图
    def get_key(self, key):
        if key[pg.K_UP]:
            self.map_offset[1] -= 4
        if key[pg.K_DOWN]:
            self.map_offset[1] += 4
        if key[pg.K_LEFT]:
            self.map_offset[0] -= 4
        if key[pg.K_RIGHT]:
            self.map_offset[0] += 4

    def get_event(self, event):
        self.measure_event(event)
        self.translate_map(event)
        # self.test_event(event)

    def translate_map(self, event):
        '''
        实现拖拽移动地图
        :param event:
        :return:
        '''
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3 and self.draw_line == False:
                self.grab_map = True
        if event.type == pg.MOUSEBUTTONUP:
            self.grab_map = False
        if event.type == pg.MOUSEMOTION:
            if self.grab_map == True:
                self.map_offset[0] -= event.rel[0]
                self.map_offset[1] -= event.rel[1]

    def test_event(self, event):
        '''
        测试用
        :param event:
        :return:
        '''
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            x, y = self.mouse_pos_to_map_id(mouse_pos)
            # 鼠标选取单元格，并显示其状态信息
            print(self.get_hex_info(x, y))

    def measure_event(self, event):
        '''
        按住 m 键，点鼠标左键作为起点，出现红线，再次点鼠标左键，计算距离
        :param event:
        :return:
        '''
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_m:
                self.draw_line = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_m:
                self.draw_line_init()
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            if self.draw_line == True:
                if event.button == 1:
                    if self.measure_start_point == (0, 0):
                        self.measure_start_point = (mouse_pos)
                    else:
                        self.measure_end_point = (mouse_pos)
                        x1, x2 = self.mouse_pos_to_map_id(self.measure_start_point)
                        x3, x4 = self.mouse_pos_to_map_id(self.measure_end_point)
                        self.measure_distance = self.get_distance_between_hex(x1, x2, x3, x4)
                        p1, p2 = self.measure_start_point
                        p3, p4 = self.measure_end_point
                        hexes = self.get_hexes_between_hex(p1, p2, p3, p4, self.measure_distance)
                        print(self.check_observation(hexes) + ',直线距离是' + str(
                            self.measure_distance) + '个六角格,' + '分别是' + str(hexes))

        if event.type == pg.MOUSEMOTION:
            mouse_pos = pg.mouse.get_pos()
            if self.draw_line == True and self.measure_distance == 0:
                if self.measure_start_point != (0, 0):
                    self.measure_end_point = (mouse_pos)

    def font_surface(self, text, size, colour):
        '''
        简单实现文字转为
        :param text:
        :param size:
        :param colour:
        :return:
        '''
        font = pg.font.get_default_font()
        font_layer = pg.font.Font(font, size)
        font_surface = font_layer.render(text, True, colour)
        return font_surface

    def load_terrianmap(self, hex_map, map_data):
        """
        输入六角格地图，地图的表单数据，返回pygame.surface
        六角地图的绘制直接用excel的map_id，这样明显少了一步中间计算，程序会快一点
        :param hex:
        :param map_data:
        :return:
        """
        surface = pg.Surface((3000, 3000))  # 没仔细算应该取多大， 此处是随意设置够大的surface
        for i, j, k in zip(map_data.col_values(1, 1), map_data.col_values(9, 1),
                           map_data.col_values(7, 1)):  # 分别读取id，高程，地形
            i = int(i)
            j = int(j)
            k = int(k)
            x, y = self.excel_id_to_map_id(i)  # 将excel编码六角格转为行列编码id
            if x < 10:
                hex_x = '0' + str(x)
            else:
                hex_x = str(x)
            if y < 10:
                hex_y = '0' + str(y)
            else:
                hex_y = str(y)
            hex_id = hex_x + hex_y  # 六角格id
            id_text_surface = font_surface(hex_id, 10, (0, 0, 0))  # id文字图层
            elevation_text_sruface = font_surface(str(j), 10, (0, 0, 0))  # 高程图层
            off_e = self.offline_potiential.get((int(hex_x),int(hex_y)),0)
            offline_energy_surface =font_surface(str(off_e),20,(255,255,255,128))

            # 设置显示坐标范围
            # if 8 <= x <= 25 and 5 <= y <= 45:
            if 0 <= x <= 50 and 0 <= y <= 100:
                if i % 2 == 0:
                    surface.blit(hex_map['dixing' + str(j)], (i % 10000 * 54 / 2, i // 10000 * 90))  # 瓦片地图
                    surface.blit(hex_map[str(k)], (i % 10000 * 54 / 2, i // 10000 * 90))  # 地形
                    surface.blit(id_text_surface, (i % 10000 * 54 / 2 + 15, i // 10000 * 90 + 10))  #
                    surface.blit(elevation_text_sruface, (i % 10000 * 54 / 2 + 20, i // 10000 * 90 + 40))  # 高程
                    # surface.blit(offline_energy_surface,(i % 10000 * 54 / 2 + 15, i // 10000 * 90 + 20))
                else:
                    surface.blit(hex_map['dixing' + str(j)], (i % 10000 * 54 / 2, i // 10000 * 90 + 45))
                    surface.blit(hex_map[str(k)], (i % 10000 * 54 / 2, i // 10000 * 90 + 45))
                    surface.blit(id_text_surface, (i % 10000 * 54 / 2 + 15, i // 10000 * 90 + 45 + 10))
                    surface.blit(elevation_text_sruface, (i % 10000 * 54 / 2 + 20, i // 10000 * 90 + 45 + 40))
                    # surface.blit(offline_energy_surface, (i % 10000 * 54 / 2 + 15, i // 10000 * 90 + 45 + 20))

        return surface

    def map_id_to_excel_id(self, x, y):
        # 将地图的id转化为excel中的map_id
        if x % 2 == 0:
            return x // 2 * 10000 + y * 2
        else:
            return x // 2 * 10000 + y * 2 + 1

    def excel_id_to_map_id(self, excel_id):
        # 将excel中的map_id转换为地图的id
        x = excel_id // 10000 * 2
        y = excel_id % 10000
        if y % 2 == 0:
            y = y / 2
        else:
            y = y / 2 - 0.5
            x = x + 1
        return (int(x), int(y))

    def mouse_pos_to_excel_id(self, mouse_pos):
        # 根据鼠标屏幕位置范围excel中的六角格id编号
        x, y = self.mouse_pos_to_map_id(mouse_pos)
        excel_id = self.map_id_to_excel_id(x, y)
        return excel_id

    def get_neighbour(self, co_x, co_y):
        neighbour = []
        if co_x % 2 == 0:
            neighbour = [(co_x, co_y - 1), (co_x, co_y + 1), (co_x - 1, co_y - 1), (co_x - 1, co_y),
                         (co_x + 1, co_y - 1), (co_x + 1, co_y)]
        if co_x % 2 == 1:
            neighbour = [(co_x, co_y - 1), (co_x, co_y + 1), (co_x - 1, co_y), (co_x - 1, co_y + 1), (co_x + 1, co_y),
                         (co_x + 1, co_y + 1)]
        return neighbour

    def mouse_pos_to_map_id(self, mouse_pos):
        # 根据鼠标在屏幕位置返回的六角格的id（第几行第几列）
        # 公式换算参考下列网页
        # https://gamedev.stackexchange.com/questions/20742/how-can-i-implement-hexagonal-tilemap-picking-in-xna
        x, y = mouse_pos
        x = x + self.map_offset[0]
        y = y + self.map_offset[1]
        grid_width = 54
        grid_height = int(60 / 4.0 * 3)
        half_width = int(54 / 2.0)
        row = int(y / grid_height)
        row_is_odd = (row % 2 == 1)
        rel_y = y - (row * grid_height)
        if row_is_odd:
            column = int((x - half_width) / grid_width)
            rel_x = (x - (column * grid_width)) - half_width
        else:
            column = int(x / grid_width)
            rel_x = x - (column * grid_width)
        a = 60 / 4.0
        m = a / half_width
        if rel_y < -m * rel_x + a:
            row -= 1
            if not row_is_odd:
                column -= 1
        elif rel_y < m * rel_x - a:
            row -= 1
            if row_is_odd:
                column += 1
        a = row
        b = column
        return (a, b)

    def get_hex_info(self, x, y):
        # 通过地图id 得到地图单元格信息:
        excel_id = self.map_id_to_excel_id(x, y)
        table = self.map_excel_data
        # 定义一个字典，存储栅格化地形数据
        data = {}
        for i in range(1, table.nrows):
            if int(table.cell_value(i, 1)) == excel_id:
                data['map_id'] = (x, y)
                data['excel_map_id'] = int(table.cell_value(i, 1))
                data['elevation'] = table.cell_value(i, 3)  # 海拔
                data['cond'] = int(table.cell_value(i, 5))  # 地质 （0 无 6 松软地 7 道路穿过居民地）
                data['obj_step'] = int(table.cell_value(i, 6))  # 机动力消耗
                data['grid_id'] = int(table.cell_value(i, 7))  # 六角格形状id
                data['grid_type'] = int(table.cell_value(i, 8))  # 六角格类型（1 水系 2 道路 3 遮蔽）
                data['ground_id'] = int(table.cell_value(i, 9))  # 以10米为等级划分的高程
        return data

    def get_distance_between_hex(self, hex_1_x, hex_1_y, hex_2_x, hex_2_y):
        def oddr_to_cube(row, col):

            x = col - (row - (row & 1)) / 2
            z = row
            y = -x - z
            return (x, y, z)

        start = oddr_to_cube(hex_1_x, hex_1_y)
        end = oddr_to_cube(hex_2_x, hex_2_y)
        return int(max(abs(start[0] - end[0]), abs(start[1] - end[1]), abs(start[2] - end[2])))

    def get_highest_hex(self, point_1_x, point_1_y, point_2_x, point_2_y):
        n = self.get_distance_between_hex(point_1_x, point_1_y, point_2_x, point_2_y)
        hexes = self.get_hexes_between_hex(point_1_x, point_1_y, point_2_x, point_2_y, n)
        elevation = []
        for i in hexes:
            data = self.get_hex_info(*i)
            elevation.append(data['ground_id'])
            if max(elevation) > max(elevation[0], elevation[-1]):
                return max(elevation)
            else:
                return max(elevation[0], elevation[-1])

    def get_hexes_between_hex(self, point_1_x, point_1_y, point_2_x, point_2_y, n):
        # 检查起点，终点直接经过哪些六角格
        delta_x = (point_2_x - point_1_x) / n
        delta_y = (point_2_y - point_1_y) / n
        hexes = []
        for i in range(n + 1):
            hex = self.mouse_pos_to_map_id((point_1_x + i * delta_x, point_1_y + i * delta_y))
            if hex not in hexes:
                hexes.append(hex)
        return hexes

    def get_topleft_from_hex(self,co_x,co_y):
        if co_x % 2 == 0:
            topleft = (co_y * 54 + 27 - 20 - self.map_offset[0], co_x * 45 + 60 / 2 - 20 - self.map_offset[1])
        elif co_x % 2 == 1:
            topleft = (co_y * 54 + 54 - 20 - self.map_offset[0], co_x * 45 + 60 / 2 - 20 - self.map_offset[1])
        return topleft

    def check_observation(self, hexes):
        # 传入一个数组，检查起点终点是否通视，不完善
        elevation = []
        for i in hexes:
            data = self.get_hex_info(*i)
            if data['grid_type'] == 3:
                return '不通视'
            elevation.append(data['ground_id'])
        if max(elevation) > max(elevation[0], elevation[-1]):
            return '不通视'
        else:
            return '通视'

    def visibility_estimation(self, x0,y0,x1,y1):
        visibility = True

        target = self.get_hex_info(x1, y1)

        elevation_1 = self.get_hex_info(x0, y0)['ground_id']
        elevation_2 = target['ground_id']

        d = self.wargame_env.game_map.get_distance_between_hex(x0, y0, x1, y1)

        delta_elevation = (elevation_2 - elevation_1) / d

        if x0 % 2 == 0:
            start_point = (y0 * 54 + 27 + 5 - self.map_offset[0], x0 * 45 + 60 / 2 + 4 - self.map_offset[1])
        elif x0 % 2 == 1:
            start_point = (y0 * 54 + 54 + 5 - self.map_offset[0], x0 * 45 + 60 / 2 + 4 - self.map_offset[1])
        if x1 % 2 == 0:
            end_point = (y1 * 54 + 27 + 5 - self.map_offset[0], x1 * 45 + 60 / 2 + 4 - self.map_offset[1])
        elif x1 % 2 == 1:
            end_point = (y1 * 54 + 54 + 5 - self.map_offset[0], x1 * 45 + 60 / 2 + 4 - self.map_offset[1])

        delta_x = (end_point[0] - start_point[0]) / d
        delta_y = (end_point[1] - start_point[1]) / d
        # print('d=',d,'dx=',delta_x,',','dy=',delta_y,'delta_high=',delta_elevation)
        for i in range(d + 1):
            a, b = self.mouse_pos_to_map_id(
                (start_point[0] + i * delta_x, start_point[1] + i * delta_y))
            target = self.get_hex_info(a, b)
            if elevation_1 == elevation_2 and target['grid_id'] in (51, 52):
                visibility = False
            elif self.wargame_env.game_map.get_hex_info(a, b)['ground_id'] > elevation_1 + delta_elevation * i:
                visibility = False
                # print('a=', a, ' ', 'b=', b, self.wargame_env.game_map.get_hex_info(a, b)['ground_id'],elevation_1 + delta_elevation * i)
                # print(observation)
        return visibility

        # 早期编写的操作地图的功能函数---------------------------------------------

    # 通过鼠标左、右键同时按下，进行测量地图任意两点的直线距离
    def measure_distance(self):
        """
        测量距离
        """
        if self.mouse.Mouse_left_down and self.mouse.Mouse_right_down:  # 鼠标左键且右键按下时
            if self.mouse.Mouse_drag_measure == 0 or self.mouse.Mouse_drag_measure == 2:
                self.mouse.pos_start[0] = pg.mouse.get_pos()[0]
                self.mouse.pos_start[1] = pg.mouse.get_pos()[1]
                self.mouse.Mouse_drag_measure = 1
                for hex in self.hexagon_group:
                    if hex.pos_hex_rect.collidepoint(self.mouse.pos_start):
                        self.start_hex = hex
                        break
        # 测量距离
        if self.mouse.Mouse_left_down and self.mouse.Mouse_right_down and self.mouse.Mouse_drag_measure == 1:  # 左右键同时按下时
            self.mouse.pos_stop[0] = pg.mouse.get_pos()[0]
            self.mouse.pos_stop[1] = pg.mouse.get_pos()[1]
            for hex in self.hexagon_group:
                if hex.pos_hex_rect.collidepoint(self.mouse.pos_stop):
                    self.stop_hex = hex
                    break
            # 绘制两点间直线
            pg.draw.line(pg.display.get_surface(), RED_COLOUR, self.mouse.pos_start, pg.mouse.get_pos(), 2)
            # 测量两点间距离
            distance = self.distanse(self.start_hex, self.stop_hex)

            self.Draw_text(BASICFONT2, self.mouse.pos_stop[0], self.mouse.pos_stop[1], "距离:" + str(distance) + "格",
                           RED_COLOUR)
        if not self.mouse.Mouse_left_down and not self.mouse.Mouse_right_down and self.mouse.Mouse_drag_measure == 1:
            self.mouse.Mouse_drag_measure = 2  # 结束拖放

    # <editor-fold desc="实现对地图的操作：移动+缩放+">
    def manipulate_map(self):
        # 鼠标中键缩放地图
        if self.mouse.Mouse_mid_forward or self.mouse.Mouse_mid_backward or self.mouse.Mouse_mid_click:
            # 地图JPGE
            self.terrain.pos_mapA_bg_surface = pg.transform.smoothscale(self.terrain.pre_mapA_bg_surface,
                                                                        ((int(
                                                                            self.terrain.pre_mapA_rec.width * self.terrain.map_scale_ratio)),
                                                                         int(
                                                                             self.terrain.pre_mapA_rec.height * self.terrain.map_scale_ratio)))
            # 六角格
            for hex_list in self.hexagon_group:
                hex_list.pos_hex_surf = pg.transform.smoothscale(hex_list.pre_hex_surf, (
                    (int(hex_list.pre_hex_rect.width * self.terrain.map_scale_ratio)),
                    int(hex_list.pre_hex_rect.height * self.terrain.map_scale_ratio)))
                hex_list.pos_hex_rect.left = self.terrain.pos_mapA_rec.left + hex_list.pre_hex_rect.left * self.terrain.map_scale_ratio
                hex_list.pos_hex_rect.top = self.terrain.pos_mapA_rec.top + hex_list.pre_hex_rect.top * self.terrain.map_scale_ratio
            # 棋子
            for piece_list in self.pieces_group:
                piece_list.pos_piece_surf = pg.transform.smoothscale(piece_list.pre_piece_surf, (
                    (int(piece_list.pre_piece_rect.width * self.terrain.map_scale_ratio)),
                    int(piece_list.pre_piece_rect.height * self.terrain.map_scale_ratio)))
                piece_list.pos_piece_rect.left = self.terrain.pos_mapA_rec.left + piece_list.pre_piece_rect.left * self.terrain.map_scale_ratio
                piece_list.pos_piece_rect.top = self.terrain.pos_mapA_rec.top + piece_list.pre_piece_rect.top * self.terrain.map_scale_ratio
            self.mouse.Mouse_mid_forward = False
            self.mouse.Mouse_mid_backward = False

            # 鼠标右键拖放地图
        # -------------------------------------------------------------------------------
        if self.mouse.Mouse_right_down and not self.mouse.Mouse_left_down:  # 鼠标右键按下时:
            if self.mouse.Mouse_drag_map == 0 or self.mouse.Mouse_drag_map == 2:
                self.mouse.pos_start[0] = pg.mouse.get_pos()[0]
                self.mouse.pos_start[1] = pg.mouse.get_pos()[1]
                # 标记地形六角格的初始位置，随着bg_image同步移动
                for hex_list in self.hexagon_group:
                    hex_list.pos_hex_delt_x = hex_list.pos_hex_rect.left
                    hex_list.pos_hex_delt_y = hex_list.pos_hex_rect.top
                # 标记红蓝双方算子的初始位置，用于移动后的绘制
                for piece_list in self.pieces_group:
                    piece_list.pos_piece_delt_x = piece_list.pos_piece_rect.left
                    piece_list.pos_piece_delt_y = piece_list.pos_piece_rect.top
                self.mouse.Mouse_drag_map = 1  # 继续拖动
                # -------------------------------------------------------------------------------
        # 鼠标拖放地图jpg/hex/pieces
        if self.mouse.Mouse_right_down and not self.mouse.Mouse_left_down and self.mouse.Mouse_drag_map == 1:  # 右键拖放时：
            self.mouse.pos_stop[0] = pg.mouse.get_pos()[0]
            self.mouse.pos_stop[1] = pg.mouse.get_pos()[1]

            # 计算偏移量
            m_delt_x = self.mouse.pos_stop[0] - self.mouse.pos_start[0]
            m_delt_y = self.mouse.pos_stop[1] - self.mouse.pos_start[1]
            # 移动bg_image
            self.terrain.pos_mapA_rec.left = self.terrain.pos_map_delt_x + m_delt_x
            self.terrain.pos_mapA_rec.top = self.terrain.pos_map_delt_y + m_delt_y
            # 移动Hexagon六角格
            for hex_list in self.hexagon_group:
                hex_list.pos_hex_rect.left = hex_list.pos_hex_delt_x + m_delt_x
                hex_list.pos_hex_rect.top = hex_list.pos_hex_delt_y + m_delt_y
            # 移动红/蓝双方算子
            for piece_list in self.pieces_group:
                piece_list.pos_piece_rect.left = piece_list.pos_piece_delt_x + m_delt_x
                piece_list.pos_piece_rect.top = piece_list.pos_piece_delt_y + m_delt_y
            # -------------------------------------------------------------------------------
        if not self.mouse.Mouse_right_down and self.mouse.Mouse_drag_map == 1:
            self.terrain.pos_map_delt_x = self.terrain.pos_mapA_rec.left
            self.terrain.pos_map_delt_y = self.terrain.pos_mapA_rec.top
            for hex_list in self.hexagon_group:
                hex_list.pos_hex_delt_x = hex_list.pos_hex_rect.left
                hex_list.pos_hex_delt_y = hex_list.pos_hex_rect.top
            for piece_list in self.pieces_group:
                piece_list.pos_piece_delt_x = piece_list.pos_piece_rect.left
                piece_list.pos_piece_delt_y = piece_list.pos_piece_rect.top
            self.mouse.Mouse_drag_map = 2  # 结束拖放
        # -------------------------------------------------------------------------------

        # 绘制棋盘的栅格化后的六角格及其编号
        for hex_list in self.hexagon_group:
            self.screen.blit(hex_list.pos_hex_surf, hex_list.pos_hex_rect)
            # 显示栅格化hexagon白色边框
            # pos_hex_points = [(hex_list.pos_hex_rect.left, hex_list.pos_hex_rect.top + hex_list.pos_hex_rect.height * self.terrain.map_scale_ratio / 2), (hex_list.pos_hex_rect.left + hex_list.pos_hex_rect.width * self.terrain.map_scale_ratio / 4, hex_list.pos_hex_rect.top + hex_list.pos_hex_rect.height * self.terrain.map_scale_ratio), (hex_list.pos_hex_rect.left + 3 * hex_list.pos_hex_rect.width * self.terrain.map_scale_ratio / 4, hex_list.pos_hex_rect.top + hex_list.pos_hex_rect.height * self.terrain.map_scale_ratio), (hex_list.pos_hex_rect.left + hex_list.pos_hex_rect.width * self.terrain.map_scale_ratio, hex_list.pos_hex_rect.top + hex_list.pos_hex_rect.height * self.terrain.map_scale_ratio / 2), (hex_list.pos_hex_rect.left + 3 * hex_list.pos_hex_rect.width * self.terrain.map_scale_ratio / 4, hex_list.pos_hex_rect.top), (hex_list.pos_hex_rect.left + hex_list.pos_hex_rect.width * self.terrain.map_scale_ratio / 4,hex_list.pos_hex_rect.top)]
            # pg.draw.polygon(self.screen, WHITE_COLOUR, pos_hex_points, 1)
            # 显示六角格上的编号/地貌/高程
            self.Draw_text(Hex_ID_FONT, hex_list.pos_hex_rect.centerx - 20, hex_list.pos_hex_rect.centery - 15,
                           hex_list.ID)  # 编号
            self.Draw_text(Hex_ID_FONT, hex_list.pos_hex_rect.centerx - 20, hex_list.pos_hex_rect.centery,
                           hex_list.landform,
                           color=YELLOW_COLOUR)  # 地貌
            self.Draw_text(Hex_ID_FONT, hex_list.pos_hex_rect.centerx - 10, hex_list.pos_hex_rect.centery + 15,
                           hex_list.elevation)  # 高程

        # 绘制最底层的MapA的JPEG对象
        self.screen.blit(self.terrain.pos_mapA_bg_surface, self.terrain.pos_mapA_rec)

        # 绘制显示棋盘上的棋子
        for piece_list in self.pieces_group:
            self.screen.blit(piece_list.pos_piece_surf, piece_list.pos_piece_rect)
            # </editor-fold>
