import random

import pygame as pg

from platform_settings_07.control_class import font_surface
from resources.load_data import PIECES

pg.init()

suppress_sign = font_surface('S', 60, (255, 255, 255))
kill_sign = font_surface('X', 60, (255, 255, 255))

# Tab 向右缩进；Shift+Tab 向左缩进

# 高程修正,(x,y) 表示（高程差，距离）
elavation = {(1, 1): -2, (1, 2): -2, (1, 3): -1, (1, 4): -1, (1, 5): -1, (2, 1): -2, (2, 2): -2, (2, 3): -2, (2, 4): -1,
             (2, 5): -1, (2, 6): -1, (2, 7): -1, (3, 1): -3, (3, 2): -2, (3, 3): -2, (3, 4): -2, (3, 5): -1, (3, 6): -1,
             (3, 7): -1, (3, 8): -1, (3, 9): -1,
             (4, 1): -3, (4, 2): -3, (4, 3): -3, (4, 4): -2, (4, 5): -2, (4, 6): -1, (4, 7): -1, (4, 8): -1, (4, 9): -1,
             (4, 10): -1, (4, 11): -1,
             (5, 1): -4, (5, 2): -3, (5, 3): -3, (5, 4): -3, (5, 5): -2, (5, 6): -2, (5, 7): -2, (5, 8): -1, (5, 9): -1,
             (5, 10): -1, (5, 11): -1, (5, 12): -1,
             (6, 1): -4, (6, 2): -4, (6, 3): -4, (6, 4): -3, (6, 5): -3, (6, 6): -2, (6, 7): -2, (6, 8): -2, (6, 9): -1,
             (6, 10): -1, (6, 11): -1, (6, 12): -1,
             (7, 1): -5, (7, 2): -4, (7, 3): -4, (7, 4): -4, (7, 5): -3, (7, 6): -2, (7, 7): -2, (7, 8): -2, (7, 9): -2,
             (7, 10): -1, (7, 11): -1, (7, 12): -1,
             (8, 1): -5, (8, 2): -5, (8, 3): -5, (8, 4): -4, (8, 5): -3, (8, 6): -3, (8, 7): -2, (8, 8): -2, (8, 9): -2,
             (8, 10): -2, (8, 11): -2, (8, 12): -1,
             }

# 车辆战斗结果，（x,y,z）表示（车辆数,攻击等级,随机数）
result = {(1, 1, 2): 1, (1, 2, 7): 1, (1, 3, 3): 1, (1, 3, 4): 1, (1, 3, 5): 1, (1, 4, 4): 1, (1, 4, 5): 1,
          (1, 4, 6): 1, (1, 5, 5): 1, (1, 5, 6): 1, (1, 5, 7): 1, (1, 6, 2): 1, (1, 6, 3): 1, (1, 6, 5): 1,
          (1, 6, 6): 1, (1, 6, 7): 1,
          (1, 7, 2): 1, (1, 7, 4): 1, (1, 7, 5): 1, (1, 7, 6): 1, (1, 7, 7): 1, (1, 7, 8): 1, (1, 8, 2): 1,
          (1, 8, 4): 1, (1, 8, 5): 1, (1, 8, 6): 1, (1, 8, 7): 2, (1, 8, 8): 1,
          (1, 9, 2): 1, (1, 9, 3): 1, (1, 9, 4): 1, (1, 9, 5): 1, (1, 9, 6): 1, (1, 9, 7): 2, (1, 9, 9): 2,
          (1, 9, 11): 2,
          (1, 10, 2): 1, (1, 10, 3): 1, (1, 10, 4): 1, (1, 10, 5): 1, (1, 10, 6): 1, (1, 10, 7): 2, (1, 10, 9): 2,
          (1, 10, 10): 1, (1, 10, 11): 2,
          (2, 1, 4): 1, (2, 2, 3): 1, (2, 2, 4): 1, (2, 2, 5): 1, (2, 3, 5): 1, (2, 3, 6): 1, (2, 3, 7): 1,
          (2, 4, 2): 1, (2, 4, 3): 1, (2, 4, 5): 1, (2, 4, 6): 1, (2, 4, 7): 1, (2, 5, 2): 1, (2, 5, 4): 1,
          (2, 5, 5): 1, (2, 5, 6): 1, (2, 5, 7): 1, (2, 5, 8): 1,
          (2, 6, 2): 1, (2, 6, 4): 1, (2, 6, 5): 1, (2, 6, 6): 1, (2, 6, 7): 2, (2, 6, 8): 1, (2, 7, 2): 1,
          (2, 7, 3): 1, (2, 7, 4): 1, (2, 7, 5): 1, (2, 7, 6): 1, (2, 7, 7): 2, (2, 7, 8): 1, (2, 7, 9): 1,
          (2, 8, 2): 1, (2, 8, 3): 1, (2, 8, 4): 1, (2, 8, 5): 1, (2, 8, 6): 1, (2, 8, 7): 2, (2, 8, 9): 2,
          (2, 8, 10): 1, (2, 8, 11): 2,
          (2, 9, 2): 1, (2, 9, 3): 1, (2, 9, 4): 1, (2, 9, 5): 1, (2, 9, 6): 1, (2, 9, 7): 2, (2, 9, 8): 2,
          (2, 9, 9): 2, (2, 9, 10): 2,
          (2, 10, 2): 1, (2, 10, 3): 1, (2, 10, 4): 1, (2, 10, 5): 1, (2, 10, 6): 1, (2, 10, 7): 3, (2, 10, 8): 2,
          (2, 10, 9): 2, (2, 10, 10): 2, (2, 10, 12): 1,
          (3, 1, 7): 1, (3, 2, 4): 1, (3, 2, 5): 1, (3, 2, 6): 1, (3, 3, 2): 1, (3, 3, 3): 1, (3, 3, 5): 1,
          (3, 3, 6): 1, (3, 3, 7): 1, (3, 4, 2): 1, (3, 4, 4): 1, (3, 4, 5): 1, (3, 4, 6): 1, (3, 4, 7): 1,
          (3, 4, 8): 1, (3, 5, 2): 1, (3, 5, 3): 1, (3, 5, 4): 1, (3, 5, 5): 1, (3, 5, 6): 1, (3, 5, 7): 2,
          (3, 5, 8): 1, (3, 5, 9): 1, (3, 6, 2): 1, (3, 6, 3): 1, (3, 6, 4): 1, (3, 6, 5): 1, (3, 6, 6): 1,
          (3, 6, 7): 2, (3, 6, 9): 2,
          (3, 6, 10): 1, (3, 6, 11): 2, (3, 7, 2): 1, (3, 7, 3): 1, (3, 7, 4): 1, (3, 7, 5): 1, (3, 7, 6): 1,
          (3, 7, 7): 2, (3, 7, 8): 2,
          (3, 7, 9): 2, (3, 7, 10): 2, (3, 8, 2): 1, (3, 8, 3): 1, (3, 8, 4): 1, (3, 8, 5): 1, (3, 8, 6): 1,
          (3, 8, 7): 3, (3, 8, 8): 2,
          (3, 8, 9): 2, (3, 8, 10): 2, (3, 8, 12): 1, (3, 9, 2): 2, (3, 9, 3): 2, (3, 9, 4): 1, (3, 9, 5): 1,
          (3, 9, 6): 1, (3, 9, 7): 3, (3, 9, 8): 2, (3, 9, 9): 2, (3, 9, 10): 2, (3, 9, 11): 2, (3, 9, 12): 2,
          (3, 10, 2): 3, (3, 10, 3): 3, (3, 10, 4): 1, (3, 10, 5): 1, (3, 10, 6): 1, (3, 10, 7): 3, (3, 10, 8): 2,
          (3, 10, 9): 2, (3, 10, 10): 2, (3, 10, 11): 3, (3, 10, 12): 3}

# 车辆战损修正 (x,y), x为随机数，　y为防护力
vehicle_mod = {(-3, '复合装甲'): -3, (-3, '重型装甲'): -3, (-3, '中型装甲'): -2, (-3, '轻型装甲'): -1, (-3, '无装甲'): 0,
               (-2, '复合装甲'): -3, (-2, '重型装甲'): -2, (-2, '中型装甲'): -1, (-2, '轻型装甲'): 0, (-2, '无装甲'): 0,
               (-1, '复合装甲'): -3, (-1, '重型装甲'): -2, (-1, '中型装甲'): -1, (-1, '轻型装甲'): 0, (-1, '无装甲'): 0,
               (0, '复合装甲'): -3, (0, '重型装甲'): -1, (0, '中型装甲'): 0, (0, '轻型装甲'): 0, (0, '无装甲'): 0,
               (1, '复合装甲'): -2, (1, '重型装甲'): -1, (1, '中型装甲'): 0, (1, '轻型装甲'): 0, (1, '无装甲'): 0,
               (2, '复合装甲'): -2, (2, '重型装甲'): 0, (2, '中型装甲'): 0, (2, '轻型装甲'): 0, (2, '无装甲'): 0,
               (3, '复合装甲'): -1, (3, '重型装甲'): 0, (3, '中型装甲'): 0, (3, '轻型装甲'): 0, (3, '无装甲'): 1,
               (4, '复合装甲'): -1, (4, '重型装甲'): 0, (4, '中型装甲'): 0, (4, '轻型装甲'): 0, (4, '无装甲'): 1,
               (5, '复合装甲'): -1, (5, '重型装甲'): 0, (5, '中型装甲'): 0, (5, '轻型装甲'): 0, (5, '无装甲'): 1,
               (6, '复合装甲'): 0, (6, '重型装甲'): 0, (6, '中型装甲'): 0, (6, '轻型装甲'): 1, (6, '无装甲'): 1,
               (7, '复合装甲'): 0, (7, '重型装甲'): 0, (7, '中型装甲'): 0, (7, '轻型装甲'): 1, (7, '无装甲'): 1,
               (8, '复合装甲'): 0, (8, '重型装甲'): 0, (8, '中型装甲'): 0, (8, '轻型装甲'): 1, (8, '无装甲'): 1,
               (9, '复合装甲'): 0, (9, '重型装甲'): 0, (9, '中型装甲'): 1, (9, '轻型装甲'): 1, (9, '无装甲'): 1,
               (10, '复合装甲'): 0, (10, '重型装甲'): 1, (10, '中型装甲'): 1, (10, '轻型装甲'): 2, (10, '无装甲'): 2,
               (11, '复合装甲'): 1, (11, '重型装甲'): 2, (11, '中型装甲'): 2, (11, '轻型装甲'): 2, (11, '无装甲'): 2,
               (12, '复合装甲'): 2, (12, '重型装甲'): 2, (12, '中型装甲'): 3, (12, '轻型装甲'): 3, (12, '无装甲'): 3}

offline_potiential = {(1, 17): 8, (1, 20): 2, (1, 21): 3, (1, 22): 3, (1, 23): 5, (1, 25): 6, (1, 26): 5, (1, 28): 4,
                      (1, 29): 7, (1, 30): 22, (1, 31): 1, (1, 36): 2, (1, 40): 2, (3, 14): 1, (2, 15): 2, (2, 17): 1,
                      (3, 17): 3, (2, 18): 6, (2, 19): 5, (3, 19): 5, (3, 20): 1, (2, 21): 6, (3, 21): 6, (2, 22): 23,
                      (3, 22): 38, (2, 23): 26, (3, 23): 62, (2, 24): 17, (3, 24): 39, (2, 25): 10, (3, 25): 2,
                      (2, 26): 3, (3, 26): 3, (3, 27): 32, (3, 28): 9, (2, 29): 2, (3, 29): 28, (2, 30): 1, (3, 30): 10,
                      (2, 31): 11, (3, 31): 16, (2, 32): 2, (3, 32): 1, (3, 37): 2, (2, 38): 2, (3, 38): 2, (5, 7): 2,
                      (5, 13): 6, (5, 15): 3, (5, 17): 3, (5, 18): 10, (4, 19): 4, (5, 19): 8, (4, 20): 4, (5, 20): 27,
                      (4, 21): 14, (5, 21): 1, (5, 22): 2, (4, 23): 9, (5, 23): 7, (4, 24): 22, (5, 24): 3, (4, 25): 4,
                      (5, 25): 3, (5, 26): 12, (4, 27): 21, (5, 27): 208, (4, 28): 15, (5, 28): 124, (4, 29): 5,
                      (5, 29): 23, (4, 30): 1, (5, 30): 24, (5, 31): 24, (4, 32): 5, (5, 32): 25, (4, 33): 27,
                      (5, 33): 12, (4, 34): 3, (5, 34): 10, (4, 35): 6, (5, 35): 2, (4, 36): 11, (5, 36): 19,
                      (4, 37): 34, (5, 37): 14, (7, 9): 4, (6, 10): 1, (6, 11): 2, (6, 12): 16, (6, 13): 17, (6, 14): 8,
                      (7, 14): 1, (6, 15): 3, (6, 16): 3, (7, 16): 5, (6, 17): 29, (7, 17): 18, (6, 18): 4, (7, 18): 38,
                      (6, 19): 9, (7, 19): 117, (7, 20): 19, (6, 21): 6, (7, 21): 27, (6, 22): 139, (7, 22): 7,
                      (6, 23): 73, (7, 23): 12, (6, 24): 195, (7, 24): 132, (6, 25): 42, (7, 25): 21, (6, 26): 36,
                      (7, 26): 32, (6, 27): 89, (7, 27): 19, (6, 28): 88, (7, 28): 140, (6, 29): 379, (7, 29): 54,
                      (6, 30): 41, (7, 30): 26, (6, 31): 12, (7, 31): 17, (6, 32): 13, (6, 33): 4, (6, 34): 3,
                      (6, 39): 1, (9, 10): 3, (8, 13): 1, (8, 15): 7, (9, 15): 6, (8, 16): 21, (9, 16): 2, (8, 17): 32,
                      (9, 17): 55, (8, 18): 27, (9, 18): 81, (8, 19): 76, (9, 19): 12, (8, 20): 30, (9, 20): 39,
                      (8, 21): 17, (9, 21): 11, (8, 22): 48, (9, 22): 8, (8, 23): 54, (9, 23): 49, (8, 24): 306,
                      (9, 24): 13, (8, 25): 19, (9, 25): 1, (8, 26): 16, (9, 26): 2, (8, 27): 22, (9, 27): 33,
                      (8, 28): 88, (9, 28): 63, (8, 29): 61, (9, 29): 24, (8, 30): 10, (9, 30): 51, (8, 31): 38,
                      (8, 33): 3, (9, 33): 2, (8, 35): 1, (9, 39): 3, (11, 11): 13, (10, 12): 2, (11, 12): 6,
                      (10, 13): 8, (11, 13): 1, (10, 14): 5, (11, 14): 10, (10, 15): 1, (11, 15): 10, (10, 16): 20,
                      (11, 16): 11, (10, 17): 113, (11, 17): 18, (10, 18): 483, (11, 18): 4, (10, 19): 75, (11, 19): 7,
                      (10, 20): 13, (11, 20): 15, (10, 21): 20, (11, 21): 5, (10, 22): 8, (11, 22): 1, (10, 23): 6,
                      (11, 23): 8, (10, 24): 21, (11, 24): 15, (10, 25): 5, (11, 25): 10, (10, 26): 13, (11, 26): 164,
                      (10, 27): 36, (11, 27): 203, (10, 28): 180, (11, 28): 182, (10, 29): 50, (11, 29): 9,
                      (10, 30): 52, (11, 30): 6, (10, 31): 1, (11, 31): 1, (11, 32): 12, (11, 35): 1, (11, 36): 2,
                      (11, 37): 1, (10, 39): 4, (11, 40): 64, (10, 42): 3, (11, 42): 4, (10, 43): 4, (11, 43): 3,
                      (13, 8): 2, (12, 9): 5, (12, 10): 1, (13, 10): 3, (12, 11): 7, (13, 12): 3, (12, 13): 1,
                      (13, 13): 3, (12, 14): 2, (13, 14): 169, (12, 15): 3, (13, 15): 8, (12, 16): 19, (13, 16): 8,
                      (12, 17): 3, (13, 17): 3, (12, 18): 11, (13, 18): 6, (12, 19): 10, (13, 19): 42, (12, 20): 15,
                      (13, 20): 25, (12, 21): 14, (13, 21): 21, (13, 22): 12, (12, 23): 5, (13, 23): 26, (12, 24): 28,
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
                      (14, 28): 81, (15, 28): 125, (14, 29): 97, (15, 29): 6, (14, 30): 99, (15, 30): 8, (14, 31): 5,
                      (15, 31): 12, (14, 32): 2, (14, 33): 5, (15, 34): 4, (14, 35): 17, (14, 36): 7, (14, 37): 3,
                      (14, 38): 2, (14, 39): 12, (15, 39): 5, (14, 40): 2, (15, 40): 5, (14, 41): 1, (15, 41): 1,
                      (14, 43): 2, (15, 43): 5, (14, 45): 2, (15, 45): 6, (14, 47): 7, (15, 48): 14, (17, 3): 6,
                      (17, 4): 1, (17, 5): 17, (17, 6): 3, (17, 8): 13, (17, 9): 37, (17, 10): 1, (16, 11): 1,
                      (17, 11): 2, (17, 12): 76, (16, 13): 15, (17, 13): 24, (16, 14): 1, (17, 14): 6, (16, 16): 4,
                      (17, 16): 7, (16, 17): 4, (17, 17): 2, (16, 18): 29, (17, 18): 31, (16, 19): 628, (17, 19): 490,
                      (16, 20): 160, (17, 20): 73, (16, 21): 215, (17, 21): 159, (16, 22): 344, (17, 22): 314,
                      (16, 23): 789, (17, 23): 1643, (16, 24): 4515, (17, 24): 2662, (16, 25): 1118, (17, 25): 962,
                      (16, 26): 156, (17, 26): 210, (16, 27): 117, (17, 27): 139, (16, 28): 75, (17, 28): 105,
                      (16, 29): 65, (17, 29): 82, (16, 30): 7, (17, 30): 15, (16, 31): 5, (16, 32): 7, (17, 32): 4,
                      (16, 33): 1, (16, 34): 20, (17, 34): 45, (16, 35): 7, (17, 35): 8, (16, 36): 938, (17, 36): 3,
                      (17, 37): 14, (16, 38): 2, (17, 38): 2, (16, 39): 5, (17, 39): 5, (16, 40): 6, (17, 40): 6,
                      (16, 41): 1, (17, 41): 5, (17, 42): 2, (17, 43): 1, (17, 44): 9, (16, 45): 5, (16, 46): 1,
                      (17, 46): 1, (16, 47): 3, (17, 47): 1, (16, 48): 12, (17, 48): 13, (16, 49): 10, (16, 50): 3,
                      (19, 0): 1, (18, 1): 4, (19, 1): 1, (18, 2): 3, (19, 2): 9, (18, 3): 3, (19, 3): 6, (18, 4): 9,
                      (19, 4): 9, (18, 5): 9, (19, 5): 11, (18, 6): 9, (19, 6): 1, (18, 8): 7, (19, 8): 15, (18, 9): 19,
                      (18, 10): 1, (19, 10): 10, (18, 11): 3, (19, 11): 60, (18, 12): 3, (19, 12): 17, (18, 13): 1,
                      (19, 13): 4, (18, 14): 5, (19, 14): 24, (18, 15): 3, (19, 15): 22, (18, 16): 3, (19, 16): 21,
                      (18, 17): 14, (19, 17): 26, (18, 18): 19, (19, 18): 24, (18, 19): 51, (19, 19): 136,
                      (18, 20): 412, (19, 20): 98, (18, 21): 104, (19, 21): 188, (18, 22): 302, (19, 22): 601,
                      (18, 23): 391, (19, 23): 423, (18, 24): 582, (19, 24): 678, (18, 25): 2682, (19, 25): 1241,
                      (18, 26): 586, (19, 26): 206, (18, 27): 191, (19, 27): 64, (18, 28): 86, (19, 28): 375,
                      (18, 29): 282, (19, 29): 21, (18, 30): 17, (19, 30): 4, (18, 31): 2, (19, 31): 20, (18, 32): 5,
                      (19, 32): 15, (18, 33): 12, (19, 33): 6, (18, 34): 19, (19, 34): 15, (18, 35): 44, (19, 35): 100,
                      (18, 36): 35, (19, 36): 1, (18, 37): 6, (19, 37): 3, (18, 38): 18, (19, 38): 1, (18, 39): 2,
                      (18, 40): 11, (18, 41): 4, (18, 42): 5, (18, 43): 1, (18, 44): 2, (19, 45): 1, (18, 46): 5,
                      (19, 46): 1, (18, 47): 2, (19, 47): 3, (18, 50): 3, (18, 51): 3, (18, 52): 2, (19, 52): 1,
                      (21, 0): 2, (21, 1): 2, (20, 3): 1, (21, 3): 2, (20, 4): 6, (21, 4): 2, (20, 5): 6, (21, 5): 4,
                      (20, 6): 4, (20, 7): 8, (20, 8): 1, (20, 11): 5, (20, 12): 259, (21, 12): 235, (20, 13): 7,
                      (21, 13): 4, (20, 14): 6, (21, 14): 10, (20, 15): 18, (21, 15): 25, (20, 16): 9, (21, 16): 15,
                      (20, 17): 6, (21, 17): 13, (20, 18): 9, (21, 18): 22, (20, 19): 36, (21, 19): 30, (20, 20): 128,
                      (21, 20): 122, (20, 21): 121, (21, 21): 88, (20, 22): 195, (21, 22): 155, (20, 23): 377,
                      (21, 23): 598, (20, 24): 536, (21, 24): 2962, (20, 25): 1041, (21, 25): 642, (20, 26): 534,
                      (21, 26): 560, (20, 27): 577, (21, 27): 44, (20, 28): 398, (21, 28): 18, (20, 29): 23,
                      (21, 29): 16, (20, 30): 7, (21, 30): 9, (20, 31): 1, (21, 31): 3, (20, 32): 9, (21, 32): 16,
                      (20, 33): 13, (21, 33): 14, (20, 34): 10, (21, 34): 14, (20, 35): 162, (21, 35): 11, (20, 36): 1,
                      (21, 36): 19, (21, 37): 7, (21, 38): 2, (20, 39): 14, (21, 39): 7, (20, 41): 5, (20, 42): 2,
                      (21, 44): 1, (20, 45): 7, (20, 46): 5, (20, 51): 1, (20, 52): 1, (20, 53): 2, (22, 3): 7,
                      (23, 4): 3, (23, 5): 2, (23, 6): 2, (22, 7): 7, (23, 7): 5, (23, 8): 1, (22, 9): 1, (23, 9): 5,
                      (22, 10): 2, (23, 10): 4, (22, 11): 3, (23, 11): 3, (22, 12): 2, (23, 12): 3, (23, 13): 11,
                      (22, 14): 12, (23, 14): 8, (22, 15): 8, (23, 15): 87, (22, 16): 4, (23, 16): 19, (22, 17): 104,
                      (23, 17): 28, (22, 18): 30, (23, 18): 26, (22, 19): 23, (23, 19): 53, (22, 20): 230, (23, 20): 46,
                      (22, 21): 58, (23, 21): 179, (22, 22): 81, (23, 22): 262, (22, 23): 264, (23, 23): 335,
                      (22, 24): 1207, (23, 24): 175, (22, 25): 541, (23, 25): 198, (22, 26): 164, (23, 26): 231,
                      (22, 27): 271, (23, 27): 363, (22, 28): 20, (23, 28): 22, (22, 29): 7, (23, 29): 8, (22, 30): 1,
                      (23, 30): 3, (22, 31): 1, (23, 31): 3, (22, 32): 5, (23, 32): 6, (23, 33): 8, (22, 34): 3,
                      (23, 34): 5, (23, 35): 4, (22, 36): 4, (23, 36): 3, (22, 37): 2, (23, 38): 3, (23, 39): 26,
                      (22, 44): 3, (23, 44): 6, (22, 46): 1, (23, 49): 3, (24, 1): 1, (24, 4): 2, (24, 6): 1,
                      (25, 6): 1, (24, 7): 3, (24, 8): 14, (24, 9): 3, (24, 10): 4, (25, 10): 2, (24, 11): 7,
                      (25, 11): 5, (24, 12): 7, (25, 12): 1, (24, 13): 2, (25, 13): 12, (24, 14): 3, (25, 14): 5,
                      (24, 15): 22, (25, 15): 6, (24, 16): 8, (25, 16): 8, (24, 17): 9, (25, 17): 12, (24, 18): 11,
                      (25, 18): 39, (24, 19): 19, (25, 19): 37, (24, 20): 24, (25, 20): 92, (24, 21): 23, (25, 21): 37,
                      (24, 22): 28, (25, 22): 29, (24, 23): 147, (25, 23): 28, (24, 24): 30, (25, 24): 47, (24, 25): 64,
                      (25, 25): 93, (24, 26): 139, (25, 26): 164, (24, 27): 192, (25, 27): 34, (24, 28): 19,
                      (25, 28): 346, (24, 29): 11, (25, 29): 16, (24, 30): 5, (25, 30): 5, (24, 31): 3, (25, 32): 4,
                      (25, 33): 1, (24, 34): 3, (25, 34): 2, (25, 35): 4, (25, 36): 8, (24, 37): 2, (25, 37): 4,
                      (24, 38): 1, (25, 38): 3, (24, 39): 9, (25, 39): 4, (24, 40): 1, (25, 40): 11, (24, 41): 6,
                      (25, 44): 2, (25, 45): 2, (25, 51): 1, (26, 5): 2, (26, 7): 3, (26, 12): 5, (27, 12): 2,
                      (27, 13): 2, (27, 14): 1, (26, 15): 5, (27, 15): 8, (26, 16): 12, (26, 17): 11, (27, 17): 47,
                      (26, 18): 16, (27, 18): 6, (26, 19): 1, (27, 19): 29, (26, 20): 531, (27, 20): 166, (26, 21): 18,
                      (27, 21): 16, (26, 22): 14, (27, 22): 20, (26, 23): 9, (27, 23): 15, (26, 24): 29, (27, 24): 33,
                      (26, 25): 74, (27, 25): 106, (26, 26): 99, (27, 26): 132, (26, 27): 209, (27, 27): 16,
                      (26, 28): 18, (27, 28): 5, (26, 29): 9, (26, 30): 5, (27, 30): 3, (27, 31): 1, (26, 32): 2,
                      (27, 32): 7, (26, 33): 9, (27, 33): 1, (26, 35): 94, (27, 35): 10, (27, 37): 1, (26, 42): 3,
                      (27, 43): 1, (27, 49): 2, (28, 12): 11, (28, 13): 10, (28, 14): 12, (29, 14): 3, (29, 15): 17,
                      (28, 16): 23, (29, 16): 6, (28, 17): 6, (29, 17): 4, (28, 18): 31, (29, 18): 42, (28, 19): 58,
                      (29, 19): 26, (28, 20): 11, (29, 20): 50, (28, 21): 221, (29, 21): 123, (28, 22): 45,
                      (29, 22): 53, (28, 23): 8, (29, 23): 24, (28, 24): 16, (29, 24): 94, (28, 25): 44, (29, 25): 183,
                      (28, 26): 202, (29, 26): 32, (28, 27): 241, (29, 27): 8, (28, 28): 274, (29, 28): 33,
                      (28, 29): 22, (29, 29): 329, (28, 30): 5, (29, 30): 30, (28, 31): 1, (29, 31): 14, (28, 32): 11,
                      (29, 32): 6, (28, 33): 8, (28, 34): 9, (29, 34): 5, (28, 35): 9, (28, 36): 60, (29, 36): 11,
                      (29, 37): 11, (28, 38): 5, (29, 38): 1, (29, 39): 1, (28, 40): 2, (29, 40): 1, (28, 42): 1,
                      (29, 42): 5, (28, 43): 12, (28, 44): 1, (29, 44): 1, (31, 14): 4, (30, 16): 2, (31, 17): 1,
                      (30, 18): 1, (30, 19): 23, (31, 19): 7, (30, 20): 10, (31, 20): 5, (30, 21): 11, (31, 21): 105,
                      (30, 22): 116, (31, 22): 64, (30, 23): 106, (31, 23): 9, (30, 24): 161, (31, 24): 9, (30, 25): 12,
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


# 基类算子类定义

class Piece(pg.sprite.Sprite):
    '''
    1.将算子的属性分别列出，创建算子时需要输入算子坐标co_x，co_y
    2.每一种算子重新定义了一个个新的类，对应各自的算子图片
    3.定义一个type变量，作为算子名称
    '''

    def __init__(self, wargame, co_x, co_y, *group):
        super(Piece, self).__init__(*group)
        self.wargame_env = wargame
        self.player = None
        self.image = None
        self.rect = pg.Rect(0, 0, 50, 50)
        self.offset = self.wargame_env.game_map.map_offset
        self.co_x = co_x
        self.co_y = co_y
        self.type = None
        self.movement = None
        self.armor = None
        self.scope_people = None
        self.scope_vehicle = None
        self.fire_in_movement_ablity = None
        self.carry_missle_number = None
        self.state = '未机动'
        self.move_history = [(self.co_x, self.co_y), (self.co_x, self.co_y)]
        self.action_history = []
        self.hex_history = []
        self.state_history =[]
        self.goal = (12,24)


    def get_state(self):
        text = str(self.state) + '(' + str(self.co_x) + ',' + str(self.co_y) + ') ' + '机动力' + str(self.movement)
        return text

    @property
    def center_pix(self):
        if self.co_x % 2 == 0:
            center = (self.co_y * 54 + 27 + 5 - self.offset[0], self.co_x * 45 + 60 / 2 + 4 - self.offset[1])
        elif self.co_x % 2 == 1:
            center = (self.co_y * 54 + 54 + 5 - self.offset[0], self.co_x * 45 + 60 / 2 + 4 - self.offset[1])
        return center

    @property
    def topleft_pix(self):
        if self.co_x % 2 == 0:
            topleft = (self.co_y * 54 + 27 - 20 - self.offset[0], self.co_x * 45 + 60 / 2 - 20 - self.offset[1])
        elif self.co_x % 2 == 1:
            topleft = (self.co_y * 54 + 54 - 20 - self.offset[0], self.co_x * 45 + 60 / 2 - 20 - self.offset[1])
        return topleft

    def update(self, dt):
        self.movement = 6
        # 通过算子的坐标位置，更新算子位置
        if self.co_x % 2 == 0:
            center = (self.co_y * 54 + 27 + 5 - self.offset[0], self.co_x * 45 + 60 / 2 + 4 - self.offset[1])
        elif self.co_x % 2 == 1:
            center = (self.co_y * 54 + 54 + 5 - self.offset[0], self.co_x * 45 + 60 / 2 + 4 - self.offset[1])
        self.rect.center = center


    def change_to_move_state(self):
        self.state = '机动'

    def change_to_blocked_state(self):
        # 车辆进入遮蔽状态
        if self.state == '非机动':
            self.state = '遮蔽'
            if self.type in ('坦克', '战车'):
                self.movement /= 2


    @classmethod
    def Show_Polygon_line(self, m_pointlist, m_color, width):  # 绘制六边形
        main_screen = pg.display.get_surface()
        pg.draw.polygon(main_screen, m_color, m_pointlist, width)

    # 闪烁显示对象的边框动画
    def show_flash_animation(self, count_num, m_rect, m_color1, m_color2, width):
        main_screen_fight = pg.display.get_surface()
        if not count_num:
            count_num = 100
        if (count_num % 5):
            pg.draw.rect(main_screen_fight, m_color1, m_rect, width)
        else:
            pg.draw.rect(main_screen_fight, m_color2, m_rect, width)

    # 绘制边框线（默认参数的调用次序是固定的：先是标准参数，后是默认参数,因为默认参数在函数调用时不体现，防止误赋值
    @classmethod
    def Show_frame_line(self, m_rect, m_color, width):  # 绘制边框线
        main_screen = pg.display.get_surface()
        pg.draw.rect(main_screen, m_color, m_rect, width)


    # 两点间的通视判断函数---------正在制作
    # def visibility_estimation(self,,):
    #     observation = True
    #     x = piece.co_x
    #     y = piece.co_y
    #
    #     target = self.wargame_env.game_map.get_hex_info(x, y)
    #
    #     elevation_1 = self.wargame_env.game_map.get_hex_info(self.co_x, self.co_y)['ground_id']
    #     elevation_2 = target['ground_id']
    #
    #     d = self.wargame_env.game_map.get_distance_between_hex(self.co_x, self.co_y, x, y)
    #
    #     delta_elevation = (elevation_2 - elevation_1) / d
    #     start_point = self.center_pix
    #     end_point = piece.center_pix
    #     delta_x = (end_point[0] - start_point[0]) / d
    #     delta_y = (end_point[1] - start_point[1]) / d
    #     # print('d=',d,'dx=',delta_x,',','dy=',delta_y,'delta_high=',delta_elevation)
    #     for i in range(d + 1):
    #         a, b = self.wargame_env.game_map.mouse_pos_to_map_id(
    #             (start_point[0] + i * delta_x, start_point[1] + i * delta_y))
    #         target = self.wargame_env.game_map.get_hex_info(a, b)
    #         if elevation_1 == elevation_2 and target['grid_id'] in (51, 52) :
    #             observation = False
    #         elif self.wargame_env.game_map.get_hex_info(a, b)['ground_id'] > elevation_1 + delta_elevation * i:
    #             observation = False
    #             # print('a=', a, ' ', 'b=', b, self.wargame_env.game_map.get_hex_info(a, b)['ground_id'],elevation_1 + delta_elevation * i)
    #             # print(observation)
    #     return observation



    def check_observation(self, piece):
        observation = True
        x = piece.co_x
        y = piece.co_y

        target = self.wargame_env.game_map.get_hex_info(x, y)

        elevation_1 = self.wargame_env.game_map.get_hex_info(self.co_x, self.co_y)['ground_id']
        elevation_2 = target['ground_id']

        d = self.wargame_env.game_map.get_distance_between_hex(self.co_x, self.co_y, x, y)
        if d == 0:
            self.wargame_env.hud.information_label.set_text('Me_Target_in_Same_Hex')
            return observation
        delta_elevation = (elevation_2 - elevation_1) / d
        start_point = self.center_pix
        end_point = piece.center_pix
        delta_x = (end_point[0] - start_point[0]) / d
        delta_y = (end_point[1] - start_point[1]) / d
        # print('d=',d,'dx=',delta_x,',','dy=',delta_y,'delta_high=',delta_elevation)
        for i in range(d + 1):
            a, b = self.wargame_env.game_map.mouse_pos_to_map_id(
                (start_point[0] + i * delta_x, start_point[1] + i * delta_y))
            target = self.wargame_env.game_map.get_hex_info(a, b)
            if self.co_x == a and self.co_y == b:
                continue
            if x == a and y == b :
                continue
            if elevation_1 == elevation_2 and target['grid_id'] in (51, 52) :
                observation = False
            elif self.wargame_env.game_map.get_hex_info(a, b)['ground_id'] > elevation_1 + delta_elevation * i:
                observation = False
                # print('a=', a, ' ', 'b=', b, self.wargame_env.game_map.get_hex_info(a, b)['ground_id'],elevation_1 + delta_elevation * i)
                # print(observation)
        return observation

    def check_watch(self, piece):
        x = piece.co_x
        y = piece.co_y
        target = self.wargame_env.game_map.get_hex_info(x, y)
        d = self.wargame_env.game_map.get_distance_between_hex(self.co_x, self.co_y, x, y)
        if self.check_observation(piece):
            if target['grid_id'] not in (51, 52):  # 51代表城镇，52代表丛林；
                if d <= self.scope_vehicle:
                    return True
                else:
                    return False
            if target['grid_id'] in (51, 52) and piece.state == '遮蔽':
                if d <= self.scope_vehicle / 4:
                    return True
                else:
                    return False
            elif target['grid_id'] in (51, 52) or piece.state != '遮蔽':
                if d <= self.scope_vehicle / 2:
                    return True
                else:
                    return False
            elif d <= self.scope_vehicle:
                return True
            else:
                return False
        else:
            return False


# 红方算子类定义
class RTank(Piece):
    def __init__(self, wargame, co_x, co_y, *group):
        super(RTank, self).__init__(wargame, co_x, co_y, *group)
        self.player = '红方'
        self.states = ['机动', '行军', '遮蔽', '直瞄射击', '间瞄射击', '压制', '待机']
        self.state = '待机'
        self.image = PIECES['r_tank']
        self.rect = self.image.get_rect()
        self.wargame_env = wargame
        self.type = '坦克'
        self.movement = 6
        # 10个动作空间，分别是机动的六种、隐蔽、直瞄、间瞄、不动
        self.actions = ('W', 'E', 'NE', 'NW', 'SE', 'SW', 'HD', 'DF', 'IDF', 'STA')
        self.armor = '重型装甲'
        self.scope_people = 10
        self.scope_vehicle = 25
        self.fire_in_movement_ablity = True
        self.carry_missle_number = 0
        self.fire_range = 15
        self.num = 3
        self.per_tank_value = 9.0  # 每个坦克的分值
        self.done = False
        self.enermy = None


    #2021.6.26
        #1普通地形所需体力值
        self.common_move_cost = 3
        #2特殊地形所需体力值
        self.special_move_cost = 2
        #4想定边界长度
        self.map_length = 50
        #7最大速度
        self.max_speed = 200
        #8机动能力
        self.move_ability = 6
        #9行进间射击能力
        self.shoot_in_move = 1
        #10载弹能力
        self.carry_missle_ability = 3
        #11电子对抗能力
        self.electronic_counter_ability = 1
        #12导弹进攻能力
        self.missle_acttack_ability = 1
        #13武器系统攻击
        self.weapon_attack_types = {'type1':1,'type2':0.5,'type3':1.5}
        #14侦察能力
        self.scout_types = {'type1':1,'type2':0.5,'type3':1.5}

    #3坦克到夺控点的距离
    def distance_between_goal(self):
        return self.wargame_env.game_map.get_distance_between_hex(self.co_x,self.co_y,self.goal.co_x,self.goal.co_y)

    #5和目标坦克之间的距离
    def distance_between_piece(self,piece):
        return self.wargame_env.game_map.get_distance_between_hex(self.co_x,self.co_y,piece.co_x,piece.co_y)

    #6空中目标与我方目标的相对速度
    def air_object_rel_speed(self,speed):
        return speed - self.max_speed

    #15连线的最高程
    def get_max_height(self,goal):
        pass_hex = self.wargame_env.game_map.get_hexes_between_hex(self.co_x,self.co_y,goal.co_x,goal.co_y)
        height_list = []
        for hex in pass_hex:
            height = self.wargame_env.game_map.get_hex_info(hex.co_x,hex.co_y)['ground_id']
            height_list.append(height)
        return max(height_list)

    #16,17所处地形的实际地形高度
    def get_position_height(self):
        return self.wargame_env.game_map.get_hex_info(self.co_x,self.co_y)['ground_id']

    # 18周围有无一级公路
    def check_level_1_street(self):
        neighbours = self.wargame_env.game_map.get_neighbour(self.co_x, self.co_y)
        streets = []
        for hex in neighbours:
            cond = self.wargame_env.game_map.get_hex_info(hex.co_x, hex.co_y)['grid_id']
            streets.append(cond)
        for num in streets:
            if num in [x for x in range(26, 49)]:
                return 1
        return 0

    # 19周围有无二级公路
    def check_level_2_street(self):
        neighbours = self.wargame_env.game_map.get_neighbour(self.co_x, self.co_y)
        streets = []
        for hex in neighbours:
            cond = self.wargame_env.game_map.get_hex_info(hex.co_x, hex.co_y)['grid_id']
            streets.append(cond)
        for num in streets:
            if num in [x for x in range(53, 171)]:
                return 1
        return 0

    # 20周围有无城镇居民的
    def check_city_around(self):
        neighbours = self.wargame_env.game_map.get_neighbour(self.co_x,self.co_y)
        cities = []
        for hex in neighbours:
            cond = self.wargame_env.game_map.get_hex_info(hex.co_x,hex.co_y)['cond']
            cities.append(cond)
        if 3 in cities:
            return 1
        else:
            return 0


    #奖赏函数1
    def check_close_to_goal(self):
        old_position = self.move_history[-1]
        d1 = self.wargame_env.game_map.get_distance_between_hex(old_position.co_x,old_position.co_y,self.goal.co_x,self.goal.co_y)
        d2 = self.wargame_env.game_map.get_distance_between_hex(self.co_x,self.co_y,self.goal.co_x,self.goal.co_y)
        if d1 > d2:
            return 1
        else:
            return 0

    #2是否撞到地图边界
    def check_at_boundary(self):
        # 假设地图尺寸 50*60
        if self.co_x == 0 or self.co_y == 0:
            return 1
        elif self.co_x == 50:
            return 1
        elif self.co_y == 60:
            return 1
        else:
            return 0

    #3 检查是否打中敌方算子
    def check_fire_result(self):
        if self.enermy.num < 10:
            return 1
        else:
            return 0

    #4 检查是否被敌方打中
    def check_enermy_fire_result(self):
        if self.num < 10:
            return 1
        else:
            return 0

    #5 检查是否歼灭敌方算子
    def check_dead_result(self):
        if self.enermy.num <= 0:
            return 1
        else:
            return 0

    #6 检查是否歼灭情况下胜利
    def check_win_by_fire(self):
        if self.win and self.enermy.num <= 0:
            return 1
        else:
            return 0

    #7检查是否胜利
    def check_win_byself(self):
        if self.win:
            return 1
        else:
            return 0

    @property
    def trace_list(self):
        l = []
        for point in self.move_history:
            if point[0] % 2 == 0:
                new_point = (point[1] * 54 + 27 + 5 - self.offset[0], point[0] * 45 + 60 / 2 + 4 - self.offset[1])
            elif point[0] % 2 == 1:
                new_point = (point[1] * 54 + 54 + 5 - self.offset[0], point[0] * 45 + 60 / 2 + 4 - self.offset[1])
            l.append(new_point)
        return l

    @property
    def score(self):
        return self.num * 9

    def refresh(self):
        self.change_to_move_state()
        self.movement = 6


    def move_one_step(self, co_x, co_y):
        if not self.done:
            if 10 <= co_x <= 25 and 5 <= co_y <= 45:
                if (co_x, co_y) in self.wargame_env.game_map.get_neighbour(self.co_x, self.co_y):
                    self.wargame_env.hud.information_label.set_text('Red tank Move_to: %s, %s' % (co_x, co_y))
                    self.co_x, self.co_y = co_x, co_y
                    self.action_history.append('机动')
                    self.hex_history.append((co_x, co_y))
                    self.change_to_move_state()
                    self.done = not self.done
                    self.move_history.append((co_x, co_y))
            else:
                self.wargame_env.hud.information_label.set_text(co_x,co_y,'out of map')
                pass
        else:
            self.wargame_env.hud.information_label.set_text('invalid red move operation')


    # 完成红方算子基本移动功能函数
    def move_steps(self, action):
        int_co = [self.co_x, self.co_y]  # 初始化出发位置坐标，在想定中进行赋值
        end_co = [0, 0]
        if action == 1:
            end_co = [int_co[0], int_co[1] - 1]
        elif action == 2:
            end_co = [int_co[0], int_co[1] + 1]
        elif action == 3:
            if self.co_x % 2 == 0:
                end_co = [int_co[0] - 1, int_co[1]]
            elif self.co_x % 2 == 1:
                end_co = [int_co[0] - 1, int_co[1] + 1]
        elif action == 4:
            if self.co_x % 2 == 0:
                end_co = [int_co[0] - 1, int_co[1] - 1]
            elif self.co_x % 2 == 1:
                end_co = [int_co[0] - 1, int_co[1]]
        elif action == 5:
            if self.co_x % 2 == 0:
                end_co = [int_co[0] + 1, int_co[1]]
            elif self.co_x % 2 == 1:
                end_co = [int_co[0] + 1, int_co[1] + 1]
        elif action == 6:
            if self.co_x % 2 == 0:
                end_co = [int_co[0] + 1, int_co[1] - 1]
            elif self.co_x % 2 == 1:
                end_co = [int_co[0] + 1, int_co[1]]

        self.move_one_step(end_co[0], end_co[1])


    def get_goal_reward(self):
        enermy_1 = self.wargame_env.scenario.blue_tank_1
        enermy_2 = self.wargame_env.scenario.blue_tank_2

        enermy_1_to_goal = self.wargame_env.game_map.get_distance_between_hex(enermy_1.co_x, enermy_1.co_y, self.goal[0],
                                                                            self.goal[1])
        enermy_2_to_goal = self.wargame_env.game_map.get_distance_between_hex(enermy_2.co_x, enermy_2.co_y, self.goal[0],
                                                                            self.goal[1])
        if enermy_1_to_goal != 1 and self.co_x == self.goal[0] and self.co_y == self.goal[1]:
            win_result = 80
        elif enermy_2_to_goal != 1 and self.co_x == self.goal[0] and self.co_y == self.goal[1]:
            win_result = 80
        else:
            win_result = 0
        return win_result

    # 计算坐标位置相应的高程
    def get_xyz(self):
        z = self.wargame_env.game_map.get_hex_info(self.co_x, self.co_y)['ground_id']
        return [self.co_x, self.co_y, z]




    def get_piece_state(self):
        return [[self.co_x, self.co_y], self.state, self.num]

    def march_one_step(self, x, y):
        start = self.wargame_env.game_map.get_hex_info(self.co_x, self.co_y)
        end = self.wargame_env.game_map.get_hex_info(x, y)
        if end['grid_type'] == start['grid_type'] == 2 and self.movement >= 0.5:
            self.co_x, self.co_y = x, y
            self.movement -= 0.5

    def change_to_supress_state(self):
        self.state = '压制'

    def change_to_march_state(self):
        self.state = '行军'

    def change_to_hide_state(self):
        if not self.done:
            self.action_history.append('遮蔽')
            self.hex_history.append((self.co_x,self.co_y))
            self.state = '遮蔽'
            self.done = not self.done
            self.wargame_env.hud.information_label.set_text('Red_Hide')
        else:
            self.wargame_env.hud.information_label.set_text('invalid red hide operation')

    def change_to_move_state(self):
        self.state = '机动'

    def change_to_fire_state(self):
        self.state = '直瞄射击'

    def change_to_in_fire_state(self):
        self.state = '间瞄射击'

    def check_rank(self,enermy):
        distance = self.wargame_env.game_map.get_distance_between_hex(self.co_x, self.co_y, enermy.co_x, enermy.co_y)
        if distance <= 2:
            rank = 10
        elif distance <= 5:
            rank = 9
        elif distance <= 7:
            rank = 8
        elif distance <= 10:
            rank = 7
        elif distance == 11:
            rank = 6
        else:
            rank = 2
        data_1 = self.wargame_env.game_map.get_hex_info(self.co_x, self.co_y)
        data_2 = self.wargame_env.game_map.get_hex_info(enermy.co_x, enermy.co_y)
        elavation_1 = data_1['ground_id'] / 10
        elavation_2 = data_2['ground_id'] / 10
        num = int(elavation_2 - elavation_1)
        if num > 0:
            elavation_modify = elavation.get((num, distance), 0)
        else:
            elavation_modify = 0
        rank += elavation_modify
        return rank

    def direct_fire(self,enermy):
        if not self.done:
            self.enermy = enermy
            distance = self.wargame_env.game_map.get_distance_between_hex(self.co_x, self.co_y, enermy.co_x, enermy.co_y)
            observation = self.check_watch(enermy)
            if observation and distance <= self.fire_range and self.movement == 6:
                self.action_history.append('直瞄射击')
                self.hex_history.append((enermy.co_x, enermy.co_y))
                self.done = not self.done
                self.change_to_fire_state()
                # print('Red fire')
                if distance <= 2:
                    rank = 10
                elif distance <= 5:
                    rank = 9
                elif distance <= 7:
                    rank = 8
                elif distance <= 10:
                    rank = 7
                elif distance == 11:
                    rank = 6
                else:
                    rank = 2
                data_1 = self.wargame_env.game_map.get_hex_info(self.co_x, self.co_y)
                data_2 = self.wargame_env.game_map.get_hex_info(enermy.co_x, enermy.co_y)
                elavation_1 = data_1['ground_id'] / 10
                elavation_2 = data_2['ground_id'] / 10
                num = int(elavation_2 - elavation_1)
                if num > 0:
                    elavation_modify = elavation.get((num, distance), 0)
                else:
                    elavation_modify = 0
                rank += elavation_modify
                import random
                a = random.randint(1, 6)
                b = random.randint(1, 6)
                c = a + b
                judge_result = result.get((self.num, rank, c), 0)
                a = random.randint(1, 6)
                b = random.randint(1, 6)
                c = a + b
                if self.state == '压制':
                    c -= 1
                elif self.state == '机动':
                    c -= 1
                if data_2['cond'] == 5:
                    c -= 1
                if enermy.state == '遮蔽':
                    c -= 2
                elif enermy.state == '机动':
                    c -= 2
                elif enermy.state == '行军':
                    c += 4
                if c <= -3:
                    c = -3
                elif c >= 12:
                    c = 12
                judge_result_mod = judge_result + vehicle_mod.get((c, enermy.armor), 0)
                if judge_result_mod <= 0:
                    judge_result_mod = 0
                enermy.num -= judge_result_mod
                if enermy.num <= 0:
                    enermy.num = 0
                judge_result = 9 * judge_result_mod
                self.wargame_env.hud.information_label.set_text('Red_Direct_Fire,kill:',judge_result_mod,'blue save:',enermy.num)
                return judge_result
            else:
                return 0
        else:
            self.wargame_env.hud.information_label.set_text('invalid red fire operation')

    def get_punishment(self):
        # enermy = self.wargame_env.scenario.blue_piece
        # return -enermy.direct_fire()
        return 0

    def indirect_fire(self,co_x,co_y):
        if not self.done:
            self.action_history.append('间瞄射击')
            self.hex_history.append((co_x,co_y))
            self.done = not self.done
            self.wargame_env.hud.information_label.set_text('red indirect fire at %s,%s'%(co_x,co_y))
        else:
            self.wargame_env.hud.information_label.set_text('invalid red indirect fire operation')

    def indirect_fire_judge(self,co_x,co_y):
        if self.wargame_env.scenario.blue_tank_1.co_x == co_x and self.wargame_env.scenario.blue_tank_1.co_y == co_y:
            enermy_1 = self.wargame_env.scenario.blue_tank_1
        if self.wargame_env.scenario.blue_tank_2.co_x == co_x and self.wargame_env.scenario.blue_tank_2.co_y == co_y:
            enermy_2 = self.wargame_env.scenario.blue_tank_2
        if enermy_1:
            result_num = 0
            result_1 = 0
            a1= random.randint(1, 6)
            a2 = random.randint(1, 6)
            a = a1+a2
            judge_result = None
            if a == 2 or a ==3 or a ==11 or a ==12:
                judge_result = "deviation"
            else:
                judge_result = "hit"
            b1 = random.randint(1, 6)
            b2 = random.randint(1, 6)
            b = b1+b2
            # 按中型火炮进行设置
            if judge_result == "hit":
                if b == 2: result_num = 3
                if b == 3: result_num = 2
                if b == 4 or b ==5 or b ==6 or b ==11 or b ==12: result_num = 1
                if b == 7 or b ==8 or b ==9: result_num = 0  # -1代表压制效果
                if b == 10: result_num = 2
            elif judge_result == "deviation":
                if b == 2:
                    result_num = 1
                elif b == 3 or b ==7 or b ==10 or b ==11 or b ==12:
                    result_num = 0
                else:
                    result_num = 0
            result_1 = result_num *self.per_tank_value
            enermy_1.num -= result_num
            if enermy_1.num <= 0: enermy_1.num = 0
            self.wargame_env.hud.information_label.set_text('Red_Indirect_Fire,Kill:',result_num,'Blue save:',enermy_1.num)
        if enermy_2:
            result_2 = 0
            result_num = 0
            a1 = random.randint(1, 6)
            a2 = random.randint(1, 6)
            a = a1 + a2
            judge_result = None
            if a == 2 or a ==3 or a ==11 or a ==12:
                judge_result = "deviation"
            else:
                judge_result = "hit"
            b1 = random.randint(1, 6)
            b2 = random.randint(1, 6)
            b = b1 + b2
            # 按中型火炮进行设置
            if judge_result == "hit":
                if b == 2: result_num = 3
                if b == 3: result_num = 2
                if b == 4 or b ==5 or b ==6 or b ==11 or b ==12: result_num = 1
                if b == 7 or b ==8 or b ==9: result_num = 0  # -1代表压制效果
                if b == 10: result_num = 2
            elif judge_result == "deviation":
                if b == 2:
                    result_num = 1
                elif b == 3 or b ==7 or b ==10 or b ==11 or b ==12:
                    result_num = 0
                else:
                    result_num = 0
            result_2 = result_num * self.per_tank_value
            enermy_2.num -= result_num
            if enermy_2.num <= 0: enermy_2.num = 0
# #             self.wargame_env.hud.information_label.set_text('Red_Indirect_Fire,Kill:', result_num, 'Blue save:', enermy_2.num)
# #         return result_1 + result_2
# #
# # # 战车类定义

class RVehicle(Piece):
    def __init__(self, wargame, co_x, co_y, *group):
        super(RVehicle, self).__init__(wargame, co_x, co_y, *group)
        self.image = PIECES['r_vehicle']
        self.rect = self.image.get_rect()
        self.wargame_env = wargame
        self.type = '战车'
        self.movement = 6
        self.armor = '中型装甲'
        self.score = 6
        self.scope_people = 10
        self.scope_vehicle = 25
        self.fire_in_movement_ablity = False
        self.carry_missle_number = 4


class RPlane(RTank):
    def __init__(self, wargame, co_x, co_y, *group):
        super(RTank, self).__init__(wargame, co_x, co_y, *group)
        self.image = PIECES['r_plane']
        self.num = 1


# 步兵班类定义
class RTeam(Piece):
    def __init__(self, wargame, co_x, co_y, *group):
        super(RTeam, self).__init__(wargame, co_x, co_y, *group)
        self.image = PIECES['r_team']
        self.rect = self.image.get_rect()
        self.wargame_env = wargame
        self.type = '步兵小队'
        self.movement = 1
        self.armor = None
        self.score = 3
        self.scope_people = 10
        self.scope_vehicle = 25
        self.fire_in_movement_ablity = False
        self.carry_missle_number = 4


# 蓝方算子类定义
class BTank(Piece):
    def __init__(self, wargame, co_x, co_y, *group):
        super(BTank, self).__init__(wargame, co_x, co_y, *group)
        self.player = '蓝方'
        self.states = ['机动', '行军', '遮蔽', '直瞄射击', '间瞄射击', '待机']
        self.state = '待机'
        self.image = PIECES['b_tank']
        self.type = '坦克'
        self.movement = 6
        self.actions = ('W', 'E', 'NE', 'NW', 'SE', 'SW', 'HD', 'DF', 'IDF', 'STA')
        self.armor = '复合装甲'
        self.scope_people = 10
        self.scope_vehicle = 25
        self.fire_in_movement_ablity = True
        self.carry_missle_number = 0
        self.fire_range = 18
        self.num = 3
        self.per_tank_value = 10  # 每辆坦克分值
        self.done = False
        self.enermy = None

        # 1普通地形所需体力值
        self.common_move_cost = 3
        # 2特殊地形所需体力值
        self.special_move_cost = 2
        # 4想定边界长度
        self.map_length = 50
        # 7最大速度
        self.max_speed = 200
        # 8机动能力
        self.move_ability = 6
        # 9行进间射击能力
        self.shoot_in_move = 1
        # 10载弹能力
        self.carry_missle_ability = 3
        # 11电子对抗能力
        self.electronic_counter_ability = 1
        # 12导弹进攻能力
        self.missle_acttack_ability = 1
        # 13武器系统攻击
        self.weapon_attack_types = {'type1': 1, 'type2': 0.5, 'type3': 1.5}
        # 14侦察能力
        self.scout_types = {'type1': 1, 'type2': 0.5, 'type3': 1.5}

    # 3坦克到夺控点的距离
    def distance_between_goal(self):
        return self.wargame_env.game_map.get_distance_between_hex(self.co_x, self.co_y, self.goal[0], self.goal[1])

    # 5和目标坦克之间的距离
    def distance_between_piece(self, piece):
        return self.wargame_env.game_map.get_distance_between_hex(self.co_x, self.co_y, piece.co_x, piece.co_y)

    # 6空中目标与我方目标的相对速度
    def air_object_rel_speed(self, speed):
        return speed - self.max_speed

    # 15连线的最高程
    def get_max_height(self, goal):
        pass_hex = self.wargame_env.game_map.get_hexes_between_hex(self.co_x, self.co_y, goal.co_x, goal.co_y)
        height_list = []
        for hex in pass_hex:
            height = self.wargame_env.game_map.get_hex_info(hex.co_x, hex.co_y)['ground_id']
            height_list.append(height)
        return max(height_list)

    # 16,17所处地形的实际地形高度
    def get_position_height(self):
        return self.wargame_env.game_map.get_hex_info(self.co_x, self.co_y)['ground_id']

    # 18周围有无一级公路
    def check_level_1_street(self):
        neighbours = self.wargame_env.game_map.get_neighbour(self.co_x, self.co_y)
        streets = []
        for hex in neighbours:
            cond = self.wargame_env.game_map.get_hex_info(hex.co_x, hex.co_y)['grid_id']
            streets.append(cond)
        for num in streets:
            if num in [x for x in range(26, 49)]:
                return 1
        return 0

    # 19周围有无二级公路
    def check_level_2_street(self):
        neighbours = self.wargame_env.game_map.get_neighbour(self.co_x, self.co_y)
        streets = []
        for hex in neighbours:
            cond = self.wargame_env.game_map.get_hex_info(hex.co_x, hex.co_y)['grid_id']
            streets.append(cond)
        for num in streets:
            if num in [x for x in range(53, 171)]:
                return 1
        return 0

    # 20周围有无城镇居民的
    def check_city_around(self):
        neighbours = self.wargame_env.game_map.get_neighbour(self.co_x, self.co_y)
        cities = []
        for hex in neighbours:
            cond = self.wargame_env.game_map.get_hex_info(hex.co_x, hex.co_y)['cond']
            cities.append(cond)
        if 3 in cities:
            return 1
        else:
            return 0

    # 奖赏函数1
    def check_close_to_goal(self):
        old_position = self.move_history[-1]
        d1 = self.wargame_env.game_map.get_distance_between_hex(old_position.co_x, old_position.co_y, self.goal.co_x,
                                                                self.goal.co_y)
        d2 = self.wargame_env.game_map.get_distance_between_hex(self.co_x, self.co_y, self.goal.co_x, self.goal.co_y)
        if d1 > d2:
            return 1
        else:
            return 0

    # 2是否撞到地图边界
    def check_at_boundary(self):
        # 假设地图尺寸 50*60
        if self.co_x == 0 or self.co_y == 0:
            return 1
        elif self.co_x == 50:
            return 1
        elif self.co_y == 60:
            return 1
        else:
            return 0

    # 3 检查是否打中敌方算子
    def check_fire_result(self):
        if self.enermy.num < 10:
            return 1
        else:
            return 0

    # 4 检查是否被敌方打中
    def check_enermy_fire_result(self):
        if self.num < 10:
            return 1
        else:
            return 0

    # 5 检查是否歼灭敌方算子
    def check_dead_result(self):
        if self.enermy.num < 10:
            return 1
        else:
            return 0

    # 6 检查是否歼灭情况下胜利
    def check_win_by_fire(self):
        if self.win and self.enermy.num < 10:
            return 1
        else:
            return 0

    # 7检查是否胜利
    def check_win_byself(self):
        if self.win:
            return 1
        else:
            return 0

    @property
    def trace_list(self):
        l = []
        for point in self.move_history:
            if point[0] % 2 == 0:
                new_point = (point[1] * 54 + 27 + 5 - self.offset[0], point[0] * 45 + 60 / 2 + 4 - self.offset[1])
            elif point[0] % 2 == 1:
                new_point = (point[1] * 54 + 54 + 5 - self.offset[0], point[0] * 45 + 60 / 2 + 4 - self.offset[1])
            l.append(new_point)
        return l

    @property
    def score(self):
        return self.num * 10

    def refresh(self):
        self.change_to_move_state()
        self.movement = 6

    def march_one_step(self, x, y):
        start = self.wargame_env.game_map.get_hex_info(self.co_x, self.co_y)
        end = self.wargame_env.game_map.get_hex_info(x, y)
        if end['grid_type'] == start['grid_type'] == 2 and self.movement >= 0.5:
            self.co_x, self.co_y = x, y
            self.movement -= 0.5

    def move_one_step(self, co_x, co_y):
        if not self.done:
            self.action_history.append('机动')
            self.hex_history.append((co_x,co_y))
            self.change_to_move_state()
            self.done = not self.done
            if 10 <= co_x <= 25 and 5 <= co_y <= 45:
                if (co_x,co_y) in self.wargame_env.game_map.get_neighbour(self.co_x,self.co_y):
                    self.wargame_env.hud.information_label.set_text('blue tank Move_to: %s, %s'%(co_x,co_y))
                    self.co_x, self.co_y = co_x, co_y
                    self.move_history.append((co_x, co_y))
            else:
                pass
        else:
            self.wargame_env.hud.information_label.set_text('invalid blue move operation')


    def get_goal_reward(self):
        enermy_1 = self.wargame_env.scenario.red_tank_1
        enermy_2 = self.wargame_env.scenario.red_tank_2

        enermy_1_to_goal = self.wargame_env.game_map.get_distance_between_hex(enermy_1.co_x, enermy_1.co_y,
                                                                              self.goal[0],
                                                                              self.goal[1])
        enermy_2_to_goal = self.wargame_env.game_map.get_distance_between_hex(enermy_2.co_x, enermy_2.co_y,
                                                                              self.goal[0],
                                                                              self.goal[1])
        if enermy_1_to_goal != 1 and self.co_x == self.goal[0] and self.co_y == self.goal[1]:
            win_result = 80
        elif enermy_2_to_goal != 1 and self.co_x == self.goal[0] and self.co_y == self.goal[1]:
            win_result = 80
        else:
            win_result = 0
        return win_result

    def change_to_supress_state(self):
        self.state = '压制'

    def change_to_march_state(self):
        self.state = '行军'

    def change_to_hide_state(self):
        if not self.done:
            self.action_history.append('遮蔽')
            self.hex_history.append((self.co_x,self.co_y))
            self.state = '遮蔽'
            self.done = not self.done
            self.wargame_env.hud.information_label.set_text('blue_Hide')
        else:
            self.wargame_env.hud.information_label.set_text('invalid blue hide operation')

    def change_to_move_state(self):
        self.state = '机动'

    def change_to_fire_state(self):
        self.state = '直瞄射击'

    def change_to_in_fire_state(self):
        self.state = '间瞄射击'

    def check_rank(self,enermy):
        distance = self.wargame_env.game_map.get_distance_between_hex(self.co_x, self.co_y, enermy.co_x, enermy.co_y)
        if distance <= 2:
            rank = 10
        elif distance <= 5:
            rank = 9
        elif distance <= 7:
            rank = 8
        elif distance <= 10:
            rank = 7
        elif distance == 11:
            rank = 6
        else:
            rank = 2
        return rank

    def direct_fire(self,enermy):
        if not self.done:
            self.enermy = enermy
            distance = self.wargame_env.game_map.get_distance_between_hex(self.co_x, self.co_y, enermy.co_x, enermy.co_y)
            observation = self.check_watch(enermy)
            if observation and distance <= self.fire_range and self.movement == 6:
                self.action_history.append('直瞄射击')
                self.hex_history.append((enermy.co_x, enermy.co_y))
                self.done = not self.done
                # print('Blue fire')
                self.change_to_fire_state()
                if distance <= 2:
                    rank = 10
                elif distance <= 5:
                    rank = 9
                elif distance <= 7:
                    rank = 8
                elif distance <= 10:
                    rank = 7
                elif distance == 11:
                    rank = 6
                else:
                    rank = 2
                data_1 = self.wargame_env.game_map.get_hex_info(self.co_x, self.co_y)
                data_2 = self.wargame_env.game_map.get_hex_info(enermy.co_x, enermy.co_y)
                elavation_1 = data_1['ground_id'] / 10
                elavation_2 = data_2['ground_id'] / 10
                num = int(elavation_2 - elavation_1)
                if num > 0:
                    elavation_modify = elavation.get((num, distance), 0)
                else:
                    elavation_modify = 0
                rank += elavation_modify
                import random
                a = random.randint(1, 6)
                b = random.randint(1, 6)
                c = a + b
                judge_result = result.get((self.num, rank, c), 0)
                a = random.randint(1, 6)
                b = random.randint(1, 6)
                c = a + b
                if self.state == '压制':
                    c -= 1
                elif self.state == '机动':
                    c -= 1
                if data_2['cond'] == 5:
                    c -= 1
                if enermy.state == '遮蔽':
                    c -= 2
                elif enermy.state == '机动':
                    c -= 2
                elif enermy.state == '行军':
                    c += 4
                if c <= -3:
                    c = -3
                elif c >= 12:
                    c = 12
                judge_result_mod = judge_result + vehicle_mod.get((c, enermy.armor), 0)
                if judge_result_mod <= 0:
                    judge_result_mod = 0
                enermy.num -= judge_result_mod
                if enermy.num <= 0: enermy.num = 0
                judge_result = 10 * judge_result_mod
                self.wargame_env.hud.information_label.set_text('Blue_Direct_Fire,kill:', judge_result_mod, 'red save:', enermy.num)
                return judge_result
            else:
                return 0
        else:
            self.wargame_env.hud.information_label.set_text('invalid blue fire operation')

    def move_steps(self, action):
        # actions = ('W', 'E', 'NE', 'NW', 'SE', 'SW')
        int_co = [self.co_x, self.co_y]  # 初始化出发位置坐标，在想定中进行赋值
        end_co = [0, 0]
        if action == 'W':
            end_co = [int_co[0], int_co[1] - 1]
        elif action == 'E':
            end_co = [int_co[0], int_co[1] + 1]
        elif action == 'NE':
            if self.co_x % 2 == 0:
                end_co = [int_co[0] - 1, int_co[1]]
            elif self.co_x % 2 == 1:
                end_co = [int_co[0] - 1, int_co[1] + 1]
        elif action == 'NW':
            if self.co_x % 2 == 0:
                end_co = [int_co[0] - 1, int_co[1] - 1]
            elif self.co_x % 2 == 1:
                end_co = [int_co[0] - 1, int_co[1]]
        elif action == 'SE':
            if self.co_x % 2 == 0:
                end_co = [int_co[0] + 1, int_co[1]]
            elif self.co_x % 2 == 1:
                end_co = [int_co[0] + 1, int_co[1] + 1]
        elif action == 'SW':
            if self.co_x % 2 == 0:
                end_co = [int_co[0] + 1, int_co[1] - 1]
            elif self.co_x % 2 == 1:
                end_co = [int_co[0] + 1, int_co[1]]
        self.move_one_step(end_co[0], end_co[1])

    #
    #     reward = self.calculate_reward(end_co[0], end_co[1])
    #
    #     s_ = self.get_piece_state()
    #
    #     int_co[0] = end_co[0]
    #     int_co[1] = end_co[1]
    #
    #     done = False
    #
    #     return s_, reward, done


    def get_xyz(self):
        z = self.wargame_env.game_map.get_hex_info(self.co_x, self.co_y)['ground_id']
        return [self.co_x, self.co_y, z]

    '''
    def get_piece_state(self):
        piece_state = {}
        piece_state['blue_xyz'] = self.get_xyz()
        piece_state['blue_state'] = self.state
        piece_state['blue_score'] = self.num * 9
        enermy = self.wargame_env.scenario.red_piece
        piece_state['red_xyz'] = enermy.get_xyz()
        piece_state['red_state'] = enermy.state
        piece_state['red_score'] = enermy.num * 10
        return piece_state
    '''

    def get_piece_state(self):
        return [[self.co_x, self.co_y], self.state, self.num]

    def indirect_fire(self, co_x, co_y):
        if not self.done:
            self.action_history.append('间瞄射击')
            self.hex_history.append((co_x,co_y))
            self.done = not self.done
            self.wargame_env.hud.information_label.set_text('Blue indirect fire at %s,%s'%(co_x,co_y))
        else:
            self.wargame_env.hud.information_label.set_text('invalid blue indirect fire operation')

    def indirect_fire_judge(self, co_x, co_y):
        if self.wargame_env.scenario.red_tank_1.co_x == co_x and self.wargame_env.scenario.red_tank_1.co_y == co_y:
            enermy_1 = self.wargame_env.scenario.red_tank_1
        if self.wargame_env.scenario.red_tank_2.co_x == co_x and self.wargame_env.scenario.red_tank_2.co_y == co_y:
            enermy_2 = self.wargame_env.scenario.red_tank_2
        if enermy_1:
            result_num = 0
            result_1 = 0
            a1 = random.randint(1, 6)
            a2 = random.randint(1, 6)
            a = a1 + a2
            judge_result = None
            if a == 2 or 3 or 11 or 12:
                judge_result = "deviation"
            else:
                judge_result = "hit"
            b1 = random.randint(1, 6)
            b2 = random.randint(1, 6)
            b = b1 + b2
            # 按中型火炮进行设置
            if judge_result == "hit":
                if b == 2: result_num = 3
                if b == 3: result_num = 2
                if b == 4 or 5 or 6 or 11 or 12: result_num = 1
                if b == 7 or 8 or 9: result_num = 0  # -1代表压制效果
                if b == 10: result_num = 2
            elif judge_result == "deviation":
                if b == 2:
                    result_num = 1
                elif b == 3 or 7 or 10 or 11 or 12:
                    result_num = 0
                else:
                    result_num = 0
            result_1 = result_num * self.per_tank_value
            enermy_1.num -= result_num
            if enermy_1.num <= 0: enermy_1.num = 0
            self.wargame_env.hud.information_label.set_text('Blue_Indirect_Fire,Kill:', result_num, 'Red save:', enermy_1.num)
            if enermy_2:
                result_2 = 0
                result_num = 0
                a1 = random.randint(1, 6)
                a2 = random.randint(1, 6)
                a = a1 + a2
                judge_result = None
                if a == 2 or 3 or 11 or 12:
                    judge_result = "deviation"
                else:
                    judge_result = "hit"
                b1 = random.randint(1, 6)
                b2 = random.randint(1, 6)
                b = b1 + b2
                # 按中型火炮进行设置
                if judge_result == "hit":
                    if b == 2: result_num = 3
                    if b == 3: result_num = 2
                    if b == 4 or 5 or 6 or 11 or 12: result_num = 1
                    if b == 7 or 8 or 9: result_num = 0  # -1代表压制效果
                    if b == 10: result_num = 2
                elif judge_result == "deviation":
                    if b == 2:
                        result_num = 1
                    elif b == 3 or 7 or 10 or 11 or 12:
                        result_num = 0
                    else:
                        result_num = 0
                result_2 = result_num * self.per_tank_value
                enermy_2.num -= result_num
                if enermy_2.num <= 0: enermy_2.num = 0
                self.wargame_env.hud.information_label.set_text('Blue_Indirect_Fire,Kill:', result_num, 'Red save:', enermy_2.num)
        return result_1 + result_2


    def get_punishment(self):
        # enermy = self.wargame_env.scenario.red_piece
        # return -enermy.direct_fire()
        return 0
    def choose_action(self, observation=None):
        if self.check_win():
            result = -999999
            self.done = True
        else:
            goal_result = 0
            fire_result = 0

            # self.check_state_exist(observation)
            # action selection
            # 执行机动
            # 计算当前格子离线势能和邻居6个格子离线势能比较，如果当前格子势能最高，概率如下直瞄射击(0.5)，间瞄（0.2），遮蔽（0.2），机动（0.1）
            # 如果当前格子不是势能最高点，概率如下机动最近点（0.4），机动势能高点（0.1），直瞄（0.2），间瞄（0.2），遮蔽（0.1）

            neighbours = self.wargame_env.game_map.get_neighbour(self.co_x, self.co_y)
            e = {}
            d = {}
            current_offline_energy = offline_potiential.get((self.co_x, self.co_y), 0)
            max_energy = current_offline_energy
            for neighbour in neighbours:
                if neighbour not in self.move_history:
                    e[neighbour] = offline_potiential.get(neighbour, 0)
                    d[neighbour] = self.wargame_env.game_map.get_distance_between_hex(self.goal[0], self.goal[1],
                                                                                      neighbour[0], neighbour[1])
                    max_energy = e[neighbour] if e[neighbour] > current_offline_energy else current_offline_energy
            e_neighbour = max(e, key=e.get)
            d_neighbour = min(d, key=d.get)
            if current_offline_energy == max_energy:
                n = random.random()
                if n < 0.5:
                    self.change_to_fire_state()
                    action = self.actions[7]
                    fire_result = self.direct_fire()
                elif n < 0.7:
                    action = self.actions[8]
                    self.indirect_fire()
                elif n < 0.9:
                    action = self.actions[6]
                    self.change_to_hide_state()
                    goal_result = self.get_punishment()
                else:
                    self.change_to_move_state()
                    self.move_one_step(d_neighbour[0], d_neighbour[1])
                    goal_result = self.get_goal_reward() + self.get_punishment()
            else:
                n = random.random()
                if n < 0.4:
                    self.change_to_move_state()
                    self.move_one_step(d_neighbour[0], d_neighbour[1])
                    goal_result = self.get_goal_reward() + self.get_punishment()
                elif n < 0.5:
                    self.change_to_move_state()
                    self.move_one_step(e_neighbour[0], e_neighbour[1])
                    goal_result = self.get_goal_reward() + self.get_punishment()
                if n < 0.7:
                    self.change_to_fire_state()
                    action = self.actions[7]
                    fire_result = self.direct_fire()
                elif n < 0.9:
                    action = self.actions[8]
                    self.indirect_fire()
                else:
                    action = self.actions[6]
                    self.change_to_hide_state()
                    goal_result = self.get_punishment()

            result = goal_result + fire_result
        self.wargame_env.rounds += 1
        return self.get_piece_state(), result, self.done

        ''' #南大团队完成
        if np.random.uniform() < 0.3:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action
        '''

    '''
    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )
    '''


class Artillery(Piece):
    def __init__(self, wargame, *group):
        super(Artillery, self).__init__(wargame, *group)

    def indirect_fire(self, x, y):
        pass


class BVehicle(Piece):
    def __init__(self, wargame, co_x, co_y, *group):
        super(BVehicle, self).__init__(wargame, co_x, co_y, *group)
        self.image = PIECES['b_vehicle']
        self.rect = self.image.get_rect()
        self.wargame_env = wargame
        self.type = '战车'
        self.movement = 7
        self.armor = '重型装甲'
        self.score = 8
        self.scope_people = 10
        self.scope_vehicle = 25
        self.fire_in_movement_ablity = False
        self.carry_missle_number = 4

class BPlane(BTank):
    def __init__(self, wargame, co_x, co_y, *group):
        super(RTank, self).__init__(wargame, co_x, co_y, *group)
        self.image = PIECES['b_plane']


class BTeam(Piece):
    def __init__(self, wargame, co_x, co_y, *group):
        super(BTeam, self).__init__(wargame, co_x, co_y, *group)
        self.image = PIECES['b_team']
        self.rect = self.image.get_rect()
        self.wargame_env = wargame
        self.type = '步兵小队'
        self.movement = 1
        self.armor = None
        self.score = 4
        self.scope_people = 10
        self.scope_vehicle = 25
        self.fire_in_movement_ablity = False
        self.carry_missle_number = 4

