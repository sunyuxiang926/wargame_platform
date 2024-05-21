# -*- coding: utf-8 -*-
# @Time : 2021/5/12 19:32
import sys
import pygame as pg
from pygame.locals import *
import os
import xlrd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from deduction_config_05.ai import player_4, player_2
from deduction_config_05.ai.util import *
from deduction_config_05.ai.masac import *
from operational_assessment_06.MySql import Mysql
import random

scenario = input("请选择任务: 1.夺控、2.歼敌、3.存活、4.抢点进攻、5.据点防守"+'\n')
if scenario == "1":
    from platform_settings_07.wargame_env_01 import Wargame_env
    print("已设置任务为：1.夺控")

elif scenario == "2":
    from platform_settings_07.wargame_env_02 import Wargame_env
    print("已设置任务为：2.歼敌")

elif scenario == "3":
    from platform_settings_07.wargame_env_03 import Wargame_env
    print("已设置任务为：3.存活")

elif scenario == "4":
    from platform_settings_07.wargame_env_04 import Wargame_env
    print("已设置任务为：4.抢点进攻")

elif scenario == "5":
    from platform_settings_07.wargame_env_05 import Wargame_env
    print("已设置任务为：5.据点防守")


# from platform_settings_07.wargame_env import Wargame_env
from importlib import import_module
from ResultVisualization import ResultVisualization
import random
from datamanage.sjcl import wxz, IFN
from pieces_manager_02.piece import RTank
from pieces_manager_02.piece import BTank
# from terrain_editor_01.terrain import Game_map

mywargame_sql = Mysql("mysql")
red_done = False
blue_done = False

# 获取算子位置信息与高程信息
def get_position(piece):
    position_xyz = piece.get_xyz()
    position_ID = position_xyz[0] * 100 + position_xyz[1]
    return position_ID

# 计算不同算子间的距离与通视判断
def get_distance_between_hex(hex_1_x, hex_1_y, hex_2_x, hex_2_y):
    def oddr_to_cube(row, col):
        x = col - (row - (row & 1)) / 2
        z = row
        y = -x - z
        return (x, y, z)
    start = oddr_to_cube(hex_1_x, hex_1_y)
    end = oddr_to_cube(hex_2_x, hex_2_y)
    return int(max(abs(start[0] - end[0]), abs(start[1] - end[1]), abs(start[2] - end[2])))

# 开始上半场对抗与结果记录
def first_record_score(wargame_town):
    wargame_town.p1_red_kill_score = wargame_town.red_kill_score
    wargame_town.p1_red_get_goal_score = wargame_town.red_get_goal_score
    wargame_town.p1_red_survive_score = wargame_town.red_survive_score
    wargame_town.p1_red_win_times = wargame_town.red_win_times
    wargame_town.p2_blue_kill_score = wargame_town.blue_kill_score
    wargame_town.p2_blue_get_goal_score = wargame_town.blue_get_goal_score
    wargame_town.p2_blue_survive_score = wargame_town.blue_survive_score
    wargame_town.p2_blue_win_times = wargame_town.blue_win_times
    wargame_town.red_kill_score = 0
    wargame_town.red_get_goal_score = 0
    wargame_town.red_survive_score = 0
    wargame_town.red_win_times = 0
    wargame_town.blue_kill_score = 0
    wargame_town.blue_get_goal_score = 0
    wargame_town.blue_survive_score = 0
    wargame_town.blue_win_times = 0

# 开始下半场对抗与结果记录
def second_record_score(wargame_town):
    wargame_town.p2_red_kill_score = wargame_town.red_kill_score
    wargame_town.p2_red_get_goal_score = wargame_town.red_get_goal_score
    wargame_town.p2_red_survive_score = wargame_town.red_survive_score
    wargame_town.p2_red_win_times = wargame_town.red_win_times
    wargame_town.p1_blue_kill_score = wargame_town.blue_kill_score
    wargame_town.p1_blue_get_goal_score = wargame_town.blue_get_goal_score
    wargame_town.p1_blue_survive_score = wargame_town.blue_survive_score
    wargame_town.p1_blue_win_times = wargame_town.blue_win_times
    wargame_town.red_kill_score = 0
    wargame_town.red_get_goal_score = 0
    wargame_town.red_survive_score = 0
    wargame_town.blue_kill_score = 0
    wargame_town.blue_get_goal_score = 0
    wargame_town.blue_survive_score = 0

# 调用masac算法，初始化masac算法相关参数
masac = MASAC()
MAX_STEPS = 300
actions = [0, 1, 2, 3, 4, 5, 6, 7]
np.random.seed(2)
ep_rs = []

# 推演对抗启动与算子调用智能体基本设置
def run_wargame(p1, p2):

    RPlane9_exist = random.uniform(0.5, 1)
    RPlane10_exist = random.uniform(0.5, 1)
    RPlane11_exist = random.uniform(0.5, 1)
    RPlane12_exist = random.uniform(0.5, 1)

    print(RPlane9_exist, RPlane10_exist, RPlane11_exist, RPlane12_exist)

    # UAV_list = [1, 1, 1, 1]
    UAV_list = [1, 1, 1, 1]

    buffer_s, buffer_a, buffer_r = [], [], []
    ep_r = 0
    wargame_town = Wargame_env()
    wargame_town.p4_name = player_4.NAME
    wargame_town.p2_name = player_2.NAME
    # 对战局数
    first_half_episodes = 5000
    second_half_episodes = 0
    first_episode_num = 1
    second_episode_num = 1
    # 初始化ResultVisualization
    RV = ResultVisualization(first_half_episodes, second_half_episodes)
    # # 初始化算子信息列表
    episode_num = []
    steps = []

    R1_gaochenglist, R1_statelist, R1_positionlist, R1_speedlist, R1_attacklist,  R1_deflist = [], [], [], [], [], []
    R2_gaochenglist, R2_statelist, R2_positionlist, R2_speedlist, R2_attacklist,  R2_deflist = [], [], [], [], [], []
    R3_gaochenglist, R3_statelist, R3_positionlist, R3_speedlist, R3_attacklist,  R3_deflist = [], [], [], [], [], []
    R4_gaochenglist, R4_statelist, R4_positionlist, R4_speedlist, R4_attacklist,  R4_deflist = [], [], [], [], [], []
    R5_gaochenglist, R5_statelist, R5_positionlist, R5_speedlist, R5_attacklist,  R5_deflist = [], [], [], [], [], []
    R6_gaochenglist, R6_statelist, R6_positionlist, R6_speedlist, R6_attacklist,  R6_deflist = [], [], [], [], [], []
    R7_gaochenglist, R7_statelist, R7_positionlist, R7_speedlist, R7_attacklist,  R7_deflist = [], [], [], [], [], []
    R8_gaochenglist, R8_statelist, R8_positionlist, R8_speedlist, R8_attacklist,  R8_deflist = [], [], [], [], [], []
    R9_gaochenglist, R9_statelist, R9_positionlist, R9_speedlist, R9_attacklist,  R9_deflist = [], [], [], [], [], []
    R10_gaochenglist, R10_statelist, R10_positionlist, R10_speedlist, R10_attacklist,  R10_deflist = [], [], [], [], [], []

    B1_gaochenglist, B1_statelist, B1_positionlist, B1_speedlist, B1_attacklist,  B1_deflist = [], [], [], [], [], []
    B2_gaochenglist, B2_statelist, B2_positionlist, B2_speedlist, B2_attacklist,  B2_deflist = [], [], [], [], [], []
    B3_gaochenglist, B3_statelist, B3_positionlist, B3_speedlist, B3_attacklist,  B3_deflist = [], [], [], [], [], []
    B4_gaochenglist, B4_statelist, B4_positionlist, B4_speedlist, B4_attacklist,  B4_deflist = [], [], [], [], [], []
    B5_gaochenglist, B5_statelist, B5_positionlist, B5_speedlist, B5_attacklist,  B5_deflist = [], [], [], [], [], []
    B6_gaochenglist, B6_statelist, B6_positionlist, B6_speedlist, B6_attacklist,  B6_deflist = [], [], [], [], [], []
    B7_gaochenglist, B7_statelist, B7_positionlist, B7_speedlist, B7_attacklist,  B7_deflist = [], [], [], [], [], []
    B8_gaochenglist, B8_statelist, B8_positionlist, B8_speedlist, B8_attacklist,  B8_deflist = [], [], [], [], [], []
    B9_gaochenglist, B9_statelist, B9_positionlist, B9_speedlist, B9_attacklist,  B9_deflist = [], [], [], [], [], []
    B10_gaochenglist, B10_statelist, B10_positionlist, B10_speedlist, B10_attacklist,  B10_deflist = [], [], [], [], [], []

    R1_to_obj_distancelist, B1_to_obj_distancelist = [], []
    R2_to_obj_distancelist, B2_to_obj_distancelist = [], []
    R3_to_obj_distancelist, B3_to_obj_distancelist = [], []
    R4_to_obj_distancelist, B4_to_obj_distancelist = [], []
    R5_to_obj_distancelist, B5_to_obj_distancelist = [], []
    R6_to_obj_distancelist, B6_to_obj_distancelist = [], []
    R7_to_obj_distancelist, B7_to_obj_distancelist = [], []
    R8_to_obj_distancelist, B8_to_obj_distancelist = [], []
    R9_to_obj_distancelist, B9_to_obj_distancelist = [], []
    R10_to_obj_distancelist, B10_to_obj_distancelist = [], []

    R1_health_list, B1_health_list = [], []
    R2_health_list, B2_health_list = [], []
    R3_health_list, B3_health_list = [], []
    R4_health_list, B4_health_list = [], []
    R5_health_list, B5_health_list = [], []
    R6_health_list, B6_health_list = [], []
    R7_health_list, B7_health_list = [], []
    R8_health_list, B8_health_list = [], []
    R9_health_list, B9_health_list = [], []
    R10_health_list, B10_health_list = [], []


    # 加判断每局输赢
    war_result = []

    goal_point_list = [] #夺控点坐标列表
    timestep_list = [] #timestep坐标列表

    # 每局比赛初始化
    while first_episode_num <= first_half_episodes:
        wargame_town.rounds += 1
        timestep_list.append(wargame_town.rounds)
        #————————————————————————————————————————————————————————————————————————————
        # 每局令计数清零，判断每局单独的胜负
        wargame_town.red_win_times =0
        wargame_town.blue_win_times =0
        #————————————————————————————————————————————————————————————————————————————

        threshold1 = 0.35
        threshold2 = 0.4
        threshold3 = 0.5
        # print('回合数:', wargame_town.rounds)
        # RENDER = True

        RENDER = True
        if RENDER:
            wargame_town.render()

        # 添加基本算子并设置相关属性
        tank_1 = wargame_town.scenario.red_tank_1
        tank_2 = wargame_town.scenario.red_tank_2
        tank_3 = wargame_town.scenario.red_tank_3
        tank_4 = wargame_town.scenario.red_tank_4
        tank_5 = wargame_town.scenario.red_tank_5
        tank_6 = wargame_town.scenario.red_tank_6
        tank_7 = wargame_town.scenario.red_tank_7
        tank_8 = wargame_town.scenario.red_tank_8
        # print(tank_1.num, tank_2.num, tank_3.num, tank_4.num, tank_5.num, tank_6.num, tank_7.num, tank_8.num)

        if UAV_list[0] == 1:
            tank_9 = wargame_town.scenario.red_plane_9
        else:
            pass

        if UAV_list[1] == 1:
            tank_10 = wargame_town.scenario.red_plane_10
        else:
            pass

        if UAV_list[2] == 1:
            tank_11 = wargame_town.scenario.red_plane_11
        else:
            pass

        if UAV_list[3] == 1:
            tank_12 = wargame_town.scenario.red_plane_12
        else:
            pass

        neighbours1 = wargame_town.game_map.get_neighbour(tank_1.co_x, tank_1.co_y)
        neighbours2 = wargame_town.game_map.get_neighbour(tank_2.co_x, tank_2.co_y)
        neighbours3 = wargame_town.game_map.get_neighbour(tank_3.co_x, tank_3.co_y)
        neighbours4 = wargame_town.game_map.get_neighbour(tank_4.co_x, tank_4.co_y)
        neighbours5 = wargame_town.game_map.get_neighbour(tank_5.co_x, tank_5.co_y)
        neighbours6 = wargame_town.game_map.get_neighbour(tank_6.co_x, tank_6.co_y)
        neighbours7 = wargame_town.game_map.get_neighbour(tank_7.co_x, tank_7.co_y)
        neighbours8 = wargame_town.game_map.get_neighbour(tank_8.co_x, tank_8.co_y)

        if UAV_list[0] == 1:
            neighbours9 = wargame_town.game_map.get_neighbour(tank_9.co_x, tank_9.co_y)
        else:
            pass

        if UAV_list[1] == 1:
            neighbours10 = wargame_town.game_map.get_neighbour(tank_10.co_x, tank_10.co_y)
        else:
            pass

        if UAV_list[2] == 1:
            neighbours11 = wargame_town.game_map.get_neighbour(tank_11.co_x, tank_11.co_y)
        else:
            pass

        if UAV_list[3] == 1:
            neighbours12 = wargame_town.game_map.get_neighbour(tank_12.co_x, tank_12.co_y)
        else:
            pass

        enemytanks = [wargame_town.scenario.blue_tank_1, wargame_town.scenario.blue_tank_2,
                     wargame_town.scenario.blue_tank_3, wargame_town.scenario.blue_tank_4,
                     wargame_town.scenario.blue_tank_5, wargame_town.scenario.blue_tank_6,
                     wargame_town.scenario.blue_tank_7, wargame_town.scenario.blue_tank_8,
                     wargame_town.scenario.blue_tank_9, wargame_town.scenario.blue_tank_10]

        state1 = get_state_4(wargame_town, wargame_town.scenario.red_tank_1, enemytanks)
        state2 = get_state_4(wargame_town, wargame_town.scenario.red_tank_2, enemytanks)
        state3 = get_state_4(wargame_town, wargame_town.scenario.red_tank_3, enemytanks)
        state4 = get_state_4(wargame_town, wargame_town.scenario.red_tank_4, enemytanks)
        state5 = get_state_4(wargame_town, wargame_town.scenario.red_tank_5, enemytanks)
        state6 = get_state_4(wargame_town, wargame_town.scenario.red_tank_6, enemytanks)
        state7 = get_state_4(wargame_town, wargame_town.scenario.red_tank_7, enemytanks)
        state8 = get_state_4(wargame_town, wargame_town.scenario.red_tank_8, enemytanks)

        if UAV_list[0] == 1:
            state9 = get_state_4(wargame_town, wargame_town.scenario.red_plane_9, enemytanks)
        else:
            pass

        if UAV_list[1] == 1:
            state10 = get_state_4(wargame_town, wargame_town.scenario.red_plane_10, enemytanks)
        else:
            pass

        if UAV_list[2] == 1:
            state11 = get_state_4(wargame_town, wargame_town.scenario.red_plane_11, enemytanks)
        else:
            pass

        if UAV_list[3] == 1:
            state12 = get_state_4(wargame_town, wargame_town.scenario.red_plane_12, enemytanks)
        else:
            pass

        if wargame_town.rounds == 1:
            buffer_s1, buffer_a1, buffer_r1, buffer_s2, buffer_a2, buffer_r2, buffer_s3, buffer_a3, buffer_r3, buffer_s4, buffer_a4, buffer_r4 = [], [], [], [], [], [], [], [], [], [], [], []
            buffer_s5, buffer_a5, buffer_r5, buffer_s6, buffer_a6, buffer_r6, buffer_s7, buffer_a7, buffer_r7, buffer_s8, buffer_a8, buffer_r8 = [], [], [], [], [], [], [], [], [], [], [], []
            buffer_s9, buffer_a9, buffer_r9, buffer_s10, buffer_a10, buffer_r10, buffer_s11, buffer_a11, buffer_r11, buffer_s12, buffer_a12, buffer_r12 = [], [], [], [], [], [], [], [], [], [], [], []
            ep_r = 0

        print('------------------------------------------')
        wargame_town.scenario.red_tank_1.state_history.append(wargame_town.scenario.red_tank_1.get_piece_state())
        wargame_town.scenario.red_tank_2.state_history.append(wargame_town.scenario.red_tank_2.get_piece_state())
        wargame_town.scenario.red_tank_3.state_history.append(wargame_town.scenario.red_tank_3.get_piece_state())
        wargame_town.scenario.red_tank_4.state_history.append(wargame_town.scenario.red_tank_4.get_piece_state())
        wargame_town.scenario.red_tank_5.state_history.append(wargame_town.scenario.red_tank_5.get_piece_state())
        wargame_town.scenario.red_tank_6.state_history.append(wargame_town.scenario.red_tank_6.get_piece_state())
        wargame_town.scenario.red_tank_7.state_history.append(wargame_town.scenario.red_tank_7.get_piece_state())
        wargame_town.scenario.red_tank_8.state_history.append(wargame_town.scenario.red_tank_8.get_piece_state())

        if UAV_list[0] == 1:
            wargame_town.scenario.red_plane_9.state_history.append(wargame_town.scenario.red_plane_9.get_piece_state())
        else:
            pass

        if UAV_list[1] == 1:
            wargame_town.scenario.red_plane_10.state_history.append(wargame_town.scenario.red_plane_10.get_piece_state())
        else:
            pass

        if UAV_list[2] == 1:
            wargame_town.scenario.red_plane_11.state_history.append(wargame_town.scenario.red_plane_11.get_piece_state())
        else:
            pass

        if UAV_list[3] == 1:
            wargame_town.scenario.red_plane_12.state_history.append(wargame_town.scenario.red_plane_12.get_piece_state())
        else:
            pass

        wargame_town.scenario.blue_tank_1.state_history.append(wargame_town.scenario.blue_tank_1.get_piece_state())
        wargame_town.scenario.blue_tank_2.state_history.append(wargame_town.scenario.blue_tank_2.get_piece_state())
        wargame_town.scenario.blue_tank_3.state_history.append(wargame_town.scenario.blue_tank_3.get_piece_state())
        wargame_town.scenario.blue_tank_4.state_history.append(wargame_town.scenario.blue_tank_4.get_piece_state())
        wargame_town.scenario.blue_tank_5.state_history.append(wargame_town.scenario.blue_tank_5.get_piece_state())
        wargame_town.scenario.blue_tank_6.state_history.append(wargame_town.scenario.blue_tank_6.get_piece_state())
        wargame_town.scenario.blue_tank_7.state_history.append(wargame_town.scenario.blue_tank_7.get_piece_state())
        wargame_town.scenario.blue_tank_8.state_history.append(wargame_town.scenario.blue_tank_8.get_piece_state())
        wargame_town.scenario.blue_tank_9.state_history.append(wargame_town.scenario.blue_tank_9.get_piece_state())
        wargame_town.scenario.blue_tank_10.state_history.append(wargame_town.scenario.blue_tank_10.get_piece_state())

        wargame_town.check_indirect_fire('red')
        wargame_town.scenario.red_tank_1.done = False
        wargame_town.scenario.red_tank_2.done = False
        wargame_town.scenario.red_tank_3.done = False
        wargame_town.scenario.red_tank_4.done = False
        wargame_town.scenario.red_tank_5.done = False
        wargame_town.scenario.red_tank_6.done = False
        wargame_town.scenario.red_tank_7.done = False
        wargame_town.scenario.red_tank_8.done = False

        if UAV_list[0] == 1:
            wargame_town.scenario.red_plane_9.done = False
        else:
            pass

        if UAV_list[1] == 1:
            wargame_town.scenario.red_plane_10.done = False
        else:
            pass

        if UAV_list[2] == 1:
            wargame_town.scenario.red_plane_11.done = False
        else:
            pass

        if UAV_list[3] == 1:
            wargame_town.scenario.red_plane_12.done = False
        else:
            pass

        wargame_town.scenario.blue_tank_1.done = True
        wargame_town.scenario.blue_tank_2.done = True
        wargame_town.scenario.blue_tank_3.done = True
        wargame_town.scenario.blue_tank_4.done = True
        wargame_town.scenario.blue_tank_5.done = True
        wargame_town.scenario.blue_tank_6.done = True
        wargame_town.scenario.blue_tank_7.done = True
        wargame_town.scenario.blue_tank_8.done = True
        wargame_town.scenario.blue_tank_9.done = True
        wargame_town.scenario.blue_tank_10.done = True


        # 信息列表
        # 获取红1坦克高程、状态、位置
        R1_gaocheng = wargame_town.scenario.red_tank_1.get_xyz()
        R1_health = wargame_town.scenario.red_tank_1.num
        R1_height = R1_gaocheng[2]
        R1_position = (R1_gaocheng[0], R1_gaocheng[1])
        R1_gaochenglist.append(R1_height)
        R1_positionlist.append(R1_position)
        R1_state = wargame_town.scenario.red_tank_1.get_piece_state()
        R1_statelist.append(R1_state[1])
        R1_speedlist.append((random.randint(30, 55), 60))
        R1_attacklist.append((wargame_town.scenario.red_tank_1.carry_missle_ability,
                             wargame_town.scenario.red_tank_1.electronic_counter_ability,
                             wargame_town.scenario.red_tank_1.move_ability,
                             0.5))
        R1_deflist.append(0)

        # 获取红2坦克高程、状态、位置
        R2_gaocheng = wargame_town.scenario.red_tank_2.get_xyz()
        R2_health = wargame_town.scenario.red_tank_2.num
        R2_height = R2_gaocheng[2]
        R2_position = (R2_gaocheng[0], R2_gaocheng[1])
        R2_gaochenglist.append(R2_height)
        R2_positionlist.append(R2_position)
        R2_state = wargame_town.scenario.red_tank_2.get_piece_state()
        R2_statelist.append(R2_state[1])
        R2_speedlist.append((random.randint(25, 60), 60))
        R2_attacklist.append((wargame_town.scenario.red_tank_2.carry_missle_ability,
                              wargame_town.scenario.red_tank_2.electronic_counter_ability,
                              wargame_town.scenario.red_tank_2.move_ability,
                              1))
        R2_deflist.append(0)

        # 获取红3坦克高程、状态、位置
        R3_gaocheng = wargame_town.scenario.red_tank_3.get_xyz()
        R3_health = wargame_town.scenario.red_tank_3.num
        R3_height = R3_gaocheng[2]
        R3_position = (R3_gaocheng[0], R3_gaocheng[1])
        R3_gaochenglist.append(R3_height)
        R3_positionlist.append(R3_position)
        R3_state = wargame_town.scenario.red_tank_3.get_piece_state()
        R3_statelist.append(R3_state[1])
        R3_speedlist.append((random.randint(20, 40), 40))
        R3_attacklist.append((wargame_town.scenario.red_tank_3.carry_missle_ability,
                              wargame_town.scenario.red_tank_3.electronic_counter_ability,
                              wargame_town.scenario.red_tank_3.move_ability,
                              1.5))
        R3_deflist.append(0.3)

        # 获取红4坦克高程、状态、位置
        R4_gaocheng = wargame_town.scenario.red_tank_4.get_xyz()
        R4_health = wargame_town.scenario.red_tank_4.num
        R4_height = R4_gaocheng[2]
        R4_position = (R4_gaocheng[0], R4_gaocheng[1])
        R4_gaochenglist.append(R4_height)
        R4_positionlist.append(R4_position)
        R4_state = wargame_town.scenario.red_tank_4.get_piece_state()
        R4_statelist.append(R4_state[1])
        R4_speedlist.append((random.randint(20, 45), 50))
        R4_attacklist.append((wargame_town.scenario.red_tank_4.carry_missle_ability,
                              wargame_town.scenario.red_tank_4.electronic_counter_ability,
                              wargame_town.scenario.red_tank_4.move_ability,
                              0.5))
        R4_deflist.append(0.5)

        # 获取红5坦克高程、状态、位置
        R5_gaocheng = wargame_town.scenario.red_tank_5.get_xyz()
        R5_health = wargame_town.scenario.red_tank_5.num
        R5_height = R5_gaocheng[2]
        R5_position = (R5_gaocheng[0], R5_gaocheng[1])
        R5_gaochenglist.append(R5_height)
        R5_positionlist.append(R5_position)
        R5_state = wargame_town.scenario.red_tank_5.get_piece_state()
        R5_statelist.append(R5_state[1])
        R5_speedlist.append((random.randint(20, 40), 40))
        R5_attacklist.append((wargame_town.scenario.red_tank_5.carry_missle_ability,
                              wargame_town.scenario.red_tank_5.electronic_counter_ability,
                              wargame_town.scenario.red_tank_5.move_ability,
                              1))
        R5_deflist.append(0.7)

        # 获取红6坦克高程、状态、位置
        R6_gaocheng = wargame_town.scenario.red_tank_6.get_xyz()
        R6_health = wargame_town.scenario.red_tank_6.num
        R6_height = R6_gaocheng[2]
        R6_position = (R6_gaocheng[0], R6_gaocheng[1])
        R6_gaochenglist.append(R6_height)
        R6_positionlist.append(R6_position)
        R6_state = wargame_town.scenario.red_tank_6.get_piece_state()
        R6_statelist.append(R6_state[1])
        R6_speedlist.append((random.randint(30, 60), 60))
        R6_attacklist.append((wargame_town.scenario.red_tank_6.carry_missle_ability,
                              wargame_town.scenario.red_tank_6.electronic_counter_ability,
                              wargame_town.scenario.red_tank_6.move_ability,
                              1))
        R6_deflist.append(0)

        # 获取红7坦克高程、状态、位置
        R7_gaocheng = wargame_town.scenario.red_tank_7.get_xyz()
        R7_health = wargame_town.scenario.red_tank_7.num
        R7_height = R7_gaocheng[2]
        R7_position = (R7_gaocheng[0], R7_gaocheng[1])
        R7_gaochenglist.append(R7_height)
        R7_positionlist.append(R7_position)
        R7_state = wargame_town.scenario.red_tank_7.get_piece_state()
        R7_statelist.append(R7_state[1])
        R7_speedlist.append((random.randint(30, 55), 60))
        R7_attacklist.append((wargame_town.scenario.red_tank_7.carry_missle_ability,
                              wargame_town.scenario.red_tank_7.electronic_counter_ability,
                              wargame_town.scenario.red_tank_7.move_ability,
                              0.5))
        R7_deflist.append(0)

        # 获取红8坦克高程、状态、位置
        R8_gaocheng = wargame_town.scenario.red_tank_8.get_xyz()
        R8_health = wargame_town.scenario.red_tank_8.num
        R8_height = R8_gaocheng[2]
        R8_position = (R8_gaocheng[0], R8_gaocheng[1])
        R8_gaochenglist.append(R8_height)
        R8_positionlist.append(R8_position)
        R8_state = wargame_town.scenario.red_tank_8.get_piece_state()
        R8_statelist.append(R8_state[1])
        R8_speedlist.append((random.randint(25, 45), 50))
        R8_attacklist.append((wargame_town.scenario.red_tank_8.carry_missle_ability,
                              wargame_town.scenario.red_tank_8.electronic_counter_ability,
                              wargame_town.scenario.red_tank_8.move_ability,
                              1))
        R8_deflist.append(0.3)

        # 获取红9坦克高程、状态、位置
        R9_gaocheng = wargame_town.scenario.red_plane_9.get_xyz()
        R9_health = wargame_town.scenario.red_plane_9.num
        R9_height = R9_gaocheng[2]
        R9_position = (R9_gaocheng[0], R9_gaocheng[1])
        R9_gaochenglist.append(R9_height)
        R9_positionlist.append(R9_position)
        R9_state = wargame_town.scenario.red_plane_9.get_piece_state()
        R9_statelist.append(R9_state[1])
        R9_speedlist.append((random.randint(30, 45), 45))
        R9_attacklist.append((5, 2, 4, 1.5))
        R9_deflist.append(0.7)

        # 获取红10坦克高程、状态、位置
        R10_gaocheng = wargame_town.scenario.red_plane_10.get_xyz()
        R10_health = wargame_town.scenario.red_plane_10.num
        R10_height = R10_gaocheng[2]
        R10_position = (R10_gaocheng[0], R10_gaocheng[1])
        R10_gaochenglist.append(R10_height)
        R10_positionlist.append(R10_position)
        R10_state = wargame_town.scenario.red_plane_10.get_piece_state()
        R10_statelist.append(R10_state[1])
        R10_speedlist.append((random.randint(25, 40), 40))
        R10_attacklist.append((4, 1, 5, 1.5))
        R10_deflist.append(1)


        # 获取蓝1坦克高程、状态、位置
        B1_gaocheng = wargame_town.scenario.blue_tank_1.get_xyz()
        B1_health = wargame_town.scenario.blue_tank_1.num
        B1_height = B1_gaocheng[2]
        B1_position = (B1_gaocheng[0], B1_gaocheng[1])
        B1_gaochenglist.append(B1_height)
        B1_positionlist.append(B1_position)
        B1_state = wargame_town.scenario.blue_tank_1.get_piece_state()
        B1_statelist.append(B1_state[1])
        B1_speedlist.append((random.randint(30, 55), 60))
        B1_attacklist.append((wargame_town.scenario.blue_tank_1.carry_missle_ability,
                             wargame_town.scenario.blue_tank_1.electronic_counter_ability,
                             wargame_town.scenario.blue_tank_1.move_ability,
                             0.5))
        B1_deflist.append(0)

        # 获取蓝2坦克高程、状态、位置
        B2_gaocheng = wargame_town.scenario.blue_tank_2.get_xyz()
        B2_health = wargame_town.scenario.blue_tank_2.num
        B2_height = B2_gaocheng[2]
        B2_position = (B2_gaocheng[0], B2_gaocheng[1])
        B2_gaochenglist.append(B2_height)
        B2_positionlist.append(B2_position)
        B2_state = wargame_town.scenario.blue_tank_2.get_piece_state()
        B2_statelist.append(B2_state[1])
        B2_speedlist.append((random.randint(35, 55), 55))
        B2_attacklist.append((wargame_town.scenario.blue_tank_2.carry_missle_ability,
                             wargame_town.scenario.blue_tank_2.electronic_counter_ability,
                             wargame_town.scenario.blue_tank_2.move_ability,
                             1))
        B2_deflist.append(0)

        # 获取蓝3坦克高程、状态、位置
        B3_gaocheng = wargame_town.scenario.blue_tank_3.get_xyz()
        B3_health = wargame_town.scenario.blue_tank_3.num
        B3_height = B3_gaocheng[2]
        B3_position = (B3_gaocheng[0], B3_gaocheng[1])
        B3_gaochenglist.append(B3_height)
        B3_positionlist.append(B3_position)
        B3_state = wargame_town.scenario.blue_tank_3.get_piece_state()
        B3_statelist.append(B3_state[1])
        B3_speedlist.append((random.randint(30, 50), 50))
        B3_attacklist.append((wargame_town.scenario.blue_tank_3.carry_missle_ability,
                             wargame_town.scenario.blue_tank_3.electronic_counter_ability,
                             wargame_town.scenario.blue_tank_3.move_ability,
                             0.5))
        B3_deflist.append(0.3)

        # 获取蓝4坦克高程、状态、位置
        B4_gaocheng = wargame_town.scenario.blue_tank_4.get_xyz()
        B4_health = wargame_town.scenario.blue_tank_4.num
        B4_height = B4_gaocheng[2]
        B4_position = (B4_gaocheng[0], B4_gaocheng[1])
        B4_gaochenglist.append(B4_height)
        B4_positionlist.append(B4_position)
        B4_state = wargame_town.scenario.blue_tank_4.get_piece_state()
        B4_statelist.append(B4_state[1])
        B4_speedlist.append((random.randint(25, 45), 50))
        B4_attacklist.append((wargame_town.scenario.blue_tank_4.carry_missle_ability,
                             wargame_town.scenario.blue_tank_4.electronic_counter_ability,
                             wargame_town.scenario.blue_tank_4.move_ability,
                             1))
        B4_deflist.append(0.5)

        # 获取蓝5坦克高程、状态、位置
        B5_gaocheng = wargame_town.scenario.blue_tank_5.get_xyz()
        B5_health = wargame_town.scenario.blue_tank_5.num
        B5_height = B5_gaocheng[2]
        B5_position = (B5_gaocheng[0], B5_gaocheng[1])
        B5_gaochenglist.append(B5_height)
        B5_positionlist.append(B5_position)
        B5_state = wargame_town.scenario.blue_tank_5.get_piece_state()
        B5_statelist.append(B5_state[1])
        B5_speedlist.append((random.randint(20, 40), 40))
        B5_attacklist.append((wargame_town.scenario.blue_tank_5.carry_missle_ability,
                             wargame_town.scenario.blue_tank_5.electronic_counter_ability,
                             wargame_town.scenario.blue_tank_5.move_ability,
                             1.5))
        B5_deflist.append(0.7)

        # 获取蓝6坦克高程、状态、位置
        B6_gaocheng = wargame_town.scenario.blue_tank_6.get_xyz()
        B6_health = wargame_town.scenario.blue_tank_6.num
        B6_height = B6_gaocheng[2]
        B6_position = (B6_gaocheng[0], B6_gaocheng[1])
        B6_gaochenglist.append(B6_height)
        B6_positionlist.append(B6_position)
        B6_state = wargame_town.scenario.blue_tank_6.get_piece_state()
        B6_statelist.append(B6_state[1])
        B6_speedlist.append((random.randint(30, 55), 60))
        B6_attacklist.append((wargame_town.scenario.blue_tank_6.carry_missle_ability,
                             wargame_town.scenario.blue_tank_6.electronic_counter_ability,
                             wargame_town.scenario.blue_tank_6.move_ability,
                             0.5))
        B6_deflist.append(0)

        # 获取蓝7坦克高程、状态、位置
        B7_gaocheng = wargame_town.scenario.blue_tank_7.get_xyz()
        B7_health = wargame_town.scenario.blue_tank_7.num
        B7_height = B7_gaocheng[2]
        B7_position = (B7_gaocheng[0], B7_gaocheng[1])
        B7_gaochenglist.append(B7_height)
        B7_positionlist.append(B7_position)
        B7_state = wargame_town.scenario.blue_tank_7.get_piece_state()
        B7_statelist.append(B7_state[1])
        B7_speedlist.append((random.randint(35, 60), 60))
        B7_attacklist.append((wargame_town.scenario.blue_tank_7.carry_missle_ability,
                             wargame_town.scenario.blue_tank_7.electronic_counter_ability,
                             wargame_town.scenario.blue_tank_7.move_ability,
                             0.5))
        B7_deflist.append(0)

        # 获取蓝8坦克高程、状态、位置
        B8_gaocheng = wargame_town.scenario.blue_tank_8.get_xyz()
        B8_health = wargame_town.scenario.blue_tank_8.num
        B8_height = B8_gaocheng[2]
        B8_position = (B8_gaocheng[0], B8_gaocheng[1])
        B8_gaochenglist.append(B8_height)
        B8_positionlist.append(B8_position)
        B8_state = wargame_town.scenario.blue_tank_8.get_piece_state()
        B8_statelist.append(B8_state[1])
        B8_speedlist.append((random.randint(30, 45), 50))
        B8_attacklist.append((wargame_town.scenario.blue_tank_8.carry_missle_ability,
                              wargame_town.scenario.blue_tank_8.electronic_counter_ability,
                              wargame_town.scenario.blue_tank_8.move_ability,
                              1))
        B8_deflist.append(0.3)


        # 获取蓝9坦克高程、状态、位置
        B9_gaocheng = wargame_town.scenario.blue_tank_9.get_xyz()
        B9_health = wargame_town.scenario.blue_tank_9.num
        B9_height = B9_gaocheng[2]
        B9_position = (B9_gaocheng[0], B9_gaocheng[1])
        B9_gaochenglist.append(B9_height)
        B9_positionlist.append(B9_position)
        B9_state = wargame_town.scenario.blue_tank_9.get_piece_state()
        B9_statelist.append(B9_state[1])
        B9_speedlist.append((random.randint(20, 40), 40))
        B9_attacklist.append((wargame_town.scenario.blue_tank_9.carry_missle_ability,
                              wargame_town.scenario.blue_tank_9.electronic_counter_ability,
                              wargame_town.scenario.blue_tank_9.move_ability,
                              1.5))
        B9_deflist.append(0.7)

        # 获取蓝10坦克高程、状态、位置
        B10_gaocheng = wargame_town.scenario.blue_tank_10.get_xyz()
        B10_health = wargame_town.scenario.blue_tank_10.num
        B10_height = B10_gaocheng[2]
        B10_position = (B10_gaocheng[0], B10_gaocheng[1])
        B10_gaochenglist.append(B10_height)
        B10_positionlist.append(B10_position)
        B10_state = wargame_town.scenario.blue_tank_10.get_piece_state()
        B10_statelist.append(B10_state[1])
        B10_speedlist.append((random.randint(20, 35), 40))
        B10_attacklist.append((wargame_town.scenario.blue_tank_10.carry_missle_ability,
                              wargame_town.scenario.blue_tank_10.electronic_counter_ability,
                              wargame_town.scenario.blue_tank_10.move_ability,
                              1.5))
        B10_deflist.append(1)

        # 红蓝双方坦克算子距目标点距离
        # 设置夺控点坐标
        goal_point = (14, 24)
        goal_point_list.append(goal_point)

        R1_to_obj_distance = get_distance_between_hex(R1_gaocheng[0], R1_gaocheng[1], goal_point[0], goal_point[1])
        R1_to_obj_distancelist.append(R1_to_obj_distance)
        R2_to_obj_distance = get_distance_between_hex(R2_gaocheng[0], R2_gaocheng[1], goal_point[0], goal_point[1])
        R2_to_obj_distancelist.append(R2_to_obj_distance)
        R3_to_obj_distance = get_distance_between_hex(R3_gaocheng[0], R3_gaocheng[1], goal_point[0], goal_point[1])
        R3_to_obj_distancelist.append(R3_to_obj_distance)
        R4_to_obj_distance = get_distance_between_hex(R4_gaocheng[0], R4_gaocheng[1], goal_point[0], goal_point[1])
        R4_to_obj_distancelist.append(R4_to_obj_distance)
        R5_to_obj_distance = get_distance_between_hex(R5_gaocheng[0], R5_gaocheng[1], goal_point[0], goal_point[1])
        R5_to_obj_distancelist.append(R5_to_obj_distance)
        R6_to_obj_distance = get_distance_between_hex(R6_gaocheng[0], R6_gaocheng[1], goal_point[0], goal_point[1])
        R6_to_obj_distancelist.append(R6_to_obj_distance)
        R7_to_obj_distance = get_distance_between_hex(R7_gaocheng[0], R7_gaocheng[1], goal_point[0], goal_point[1])
        R7_to_obj_distancelist.append(R7_to_obj_distance)
        R8_to_obj_distance = get_distance_between_hex(R8_gaocheng[0], R8_gaocheng[1], goal_point[0], goal_point[1])
        R8_to_obj_distancelist.append(R8_to_obj_distance)
        R9_to_obj_distance = get_distance_between_hex(R9_gaocheng[0], R9_gaocheng[1], goal_point[0], goal_point[1])
        R9_to_obj_distancelist.append(R9_to_obj_distance)
        R10_to_obj_distance = get_distance_between_hex(R10_gaocheng[0], R10_gaocheng[1], goal_point[0], goal_point[1])
        R10_to_obj_distancelist.append(R10_to_obj_distance)

        B1_to_obj_distance = get_distance_between_hex(B1_gaocheng[0], B1_gaocheng[1], goal_point[0], goal_point[1])
        B1_to_obj_distancelist.append(B1_to_obj_distance)
        B2_to_obj_distance = get_distance_between_hex(B2_gaocheng[0], B2_gaocheng[1], goal_point[0], goal_point[1])
        B2_to_obj_distancelist.append(B2_to_obj_distance)
        B3_to_obj_distance = get_distance_between_hex(B3_gaocheng[0], B3_gaocheng[1], goal_point[0], goal_point[1])
        B3_to_obj_distancelist.append(B3_to_obj_distance)
        B4_to_obj_distance = get_distance_between_hex(B4_gaocheng[0], B4_gaocheng[1], goal_point[0], goal_point[1])
        B4_to_obj_distancelist.append(B4_to_obj_distance)
        B5_to_obj_distance = get_distance_between_hex(B5_gaocheng[0], B5_gaocheng[1], goal_point[0], goal_point[1])
        B5_to_obj_distancelist.append(B5_to_obj_distance)
        B6_to_obj_distance = get_distance_between_hex(B6_gaocheng[0], B6_gaocheng[1], goal_point[0], goal_point[1])
        B6_to_obj_distancelist.append(B6_to_obj_distance)
        B7_to_obj_distance = get_distance_between_hex(B7_gaocheng[0], B7_gaocheng[1], goal_point[0], goal_point[1])
        B7_to_obj_distancelist.append(B7_to_obj_distance)
        B8_to_obj_distance = get_distance_between_hex(B8_gaocheng[0], B8_gaocheng[1], goal_point[0], goal_point[1])
        B8_to_obj_distancelist.append(B8_to_obj_distance)
        B9_to_obj_distance = get_distance_between_hex(B9_gaocheng[0], B9_gaocheng[1], goal_point[0], goal_point[1])
        B9_to_obj_distancelist.append(B9_to_obj_distance)
        B10_to_obj_distance = get_distance_between_hex(B10_gaocheng[0], B10_gaocheng[1], goal_point[0], goal_point[1])
        B10_to_obj_distancelist.append(B10_to_obj_distance)

        R1_health_list.append(R1_health)
        R2_health_list.append(R2_health)
        R3_health_list.append(R3_health)
        R4_health_list.append(R4_health)
        R5_health_list.append(R5_health)
        R6_health_list.append(R6_health)
        R7_health_list.append(R7_health)
        R8_health_list.append(R8_health)
        R9_health_list.append(R9_health)
        R10_health_list.append(R10_health)

        B1_health_list.append(B1_health)
        B2_health_list.append(B2_health)
        B3_health_list.append(B3_health)
        B4_health_list.append(B4_health)
        B5_health_list.append(B5_health)
        B6_health_list.append(B6_health)
        B7_health_list.append(B7_health)
        B8_health_list.append(B8_health)
        B9_health_list.append(B9_health)
        B10_health_list.append(B10_health)
        # 红蓝算子坦克间距离
        # R1B1_distance = get_distance_between_hex(R1_gaocheng[0], R1_gaocheng[1], B1_gaocheng[0], B1_gaocheng[1])
        # R1B2_distance = get_distance_between_hex(R1_gaocheng[0], R1_gaocheng[1], B2_gaocheng[0], B2_gaocheng[1])
        # R2B1_distance = get_distance_between_hex(R2_gaocheng[0], R2_gaocheng[1], B1_gaocheng[0], B2_gaocheng[1])
        # R2B2_distance = get_distance_between_hex(R2_gaocheng[0], R2_gaocheng[1], B2_gaocheng[0], B2_gaocheng[1])
        # R1B1_distancelist.append(R1B1_distance)
        # R1B2_distancelist.append(R1B2_distance)
        # R2B1_distancelist.append(R2B1_distance)
        # R2B2_distancelist.append(R2B2_distance)
        # 获取并添加算子相关数据到列表
        episode_num.append(first_episode_num)
        steps.append(wargame_town.steps)
        # 初始化红方算子奖励设置
        r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        # 进行红方动作选择，增加一些随机性用于探索地图

        episode1 = 0



        # ------------RTank1-----------
        if tank_1.num>0:
            if first_episode_num < episode1:
                if tank_1.co_x == 17 and tank_1.co_y == 7:
                    num1 = 1
                else:
                    temp1 = np.random.rand()
                    if temp1 < threshold1:
                        num1 = masac.choose_action(state1)
                    elif temp1 < threshold2:
                        num1 = 6
                        tank_1.change_to_fire_state()
                        tank_1.direct_fire(enemytanks[0])
                    elif temp1 < threshold3:
                        num1 = 6
                        tank_1.change_to_fire_state()
                        tank_1.direct_fire(enemytanks[1])
                    else:
                        mind = 100
                        for i in range(len(neighbours1)):
                            d = tank_1.wargame_env.game_map.get_distance_between_hex(tank_1.goal[0], tank_1.goal[1],
                                                                                     neighbours1[i][0],
                                                                                     neighbours1[i][1])
                            if d < mind:
                                mind = d
                                number = i
                        num1 = number
            else:
                if tank_1.co_x == 17 and tank_1.co_y == 7:
                    num1 = 1
                else:
                    num1 = masac.choose_action(state1)
            # 进行红方动作选择和执行动作
            out1, result = replace_to_action1(wargame_town, wargame_town.scenario.red_tank_1, enemytanks, state1, num1)
            # 更新地图ui界面
            if RENDER:
                wargame_town.render()  # line:95
            # 进行打扫一个回合之后的战场
            # 更新红方走棋之后的棋盘状态
            state_next1 = get_state_4(wargame_town, wargame_town.scenario.red_tank_1, enemytanks)
            # 获取获胜信息
            done = wargame_town.check_win()
            r1 = get_reward4(wargame_town, wargame_town.scenario.red_tank_1, state1, state_next1, out1, done)
            buffer_s1.append(state1)
            buffer_a1.append(num1)
            buffer_r1.append(r1)
            if done or wargame_town.rounds == MAX_STEPS:
                war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                if done:
                    v_s_1 = 0
                else:
                    v_s_1 = masac.get_v(state_next1)
                discounted_r = []
                for r1 in buffer_r1[::-1]:
                    v_s_1 = r1 + GAMMA * v_s_1
                    discounted_r.append(v_s_1)
                discounted_r.reverse()
                bs, ba, br = np.vstack(buffer_s1), np.vstack(buffer_a1), np.array(discounted_r)[:, None]
                buffer_s1, buffer_a1, buffer_r1 = [], [], []
                masac.update(np.hstack((bs, ba, br)))
                if done or wargame_town.rounds == MAX_STEPS:
                    ep_rs.append(ep_r)
                    first_episode_num += 1
                    # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                    wargame_town.rounds = 0
                    wargame_town.reset()
                    # print("First Half %s :Red Win %s,Blue Win %s" % (
                    #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                    RV.data_update(wargame_town)
                    if first_episode_num % 12000 == 0 and first_episode_num != 0:
                        masac.save_model('./models_0101_4/model', first_episode_num)
                    continue
            else:
                if len(wargame_town.scenario.red_tank_1.action_history) < wargame_town.rounds:
                    wargame_town.scenario.red_tank_1.action_history.append('pass')
                    wargame_town.scenario.red_tank_1.hex_history.append((0, 0))



        # ----------RTank2-------------
        if tank_2.num>0:
            if first_episode_num < episode1:
                if tank_2.co_x == 17 and tank_2.co_y == 8:
                    num2 = 5
                else:
                    temp2 = np.random.rand()
                    if temp2 < threshold1:
                        num2 = masac.choose_action(state2)
                    elif temp2 < threshold2:
                        num2 = 6
                        tank_2.change_to_fire_state()
                        tank_2.direct_fire(enemytanks[0])
                    elif temp2 < threshold3:
                        num2 = 6
                        tank_2.change_to_fire_state()
                        tank_2.direct_fire(enemytanks[1])
                    else:
                        mind = 100
                        for i in range(len(neighbours2)):
                            d = tank_2.wargame_env.game_map.get_distance_between_hex(tank_2.goal[0], tank_2.goal[1],
                                                                                     neighbours2[i][0],
                                                                                     neighbours2[i][1])
                            if d < mind:
                                mind = d
                                number = i
                        num2 = number
                        # num = r2_road(tank_1.co_x, tank_1.co_y)

            else:
                if tank_2.co_x == 17 and tank_2.co_y == 8:
                    num2 = 5
                else:
                    num2 = masac.choose_action(state2)
            out2, result = replace_to_action1(wargame_town, wargame_town.scenario.red_tank_2, enemytanks, state2, num2)
            # 更新地图ui界面
            if RENDER:
                wargame_town.render()  # line:95
            # 进行打扫一个回合之后的战场
            # 更新红方走棋之后的棋盘状态
            state_next2 = get_state_4(wargame_town, wargame_town.scenario.red_tank_2,
                                      enemytanks)
            # 获取获胜信息
            done = wargame_town.check_win()
            # 根据红方走棋后的棋盘状态进行奖励获取
            r2 = get_reward4(wargame_town, wargame_town.scenario.red_tank_2, state2, state_next2, out2, done)
            buffer_s2.append(state2)
            buffer_a2.append(num2)
            buffer_r2.append(r2)
            if done or wargame_town.rounds == MAX_STEPS:
                war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                if done:
                    v_s_2 = 0
                else:
                    v_s_2 = masac.get_v(state_next2)
                discounted_r = []
                for r2 in buffer_r2[::-1]:
                    v_s_2 = r2 + GAMMA * v_s_2
                    discounted_r.append(v_s_2)
                discounted_r.reverse()
                bs, ba, br = np.vstack(buffer_s2), np.vstack(buffer_a2), np.array(discounted_r)[:, None]
                buffer_s2, buffer_a2, buffer_r2 = [], [], []
                masac.update(np.hstack((bs, ba, br)))
                if done or wargame_town.rounds == MAX_STEPS:
                    ep_rs.append(ep_r)
                    first_episode_num += 1
                    # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                    wargame_town.rounds = 0
                    wargame_town.reset()
                    # print("First Half %s :Red Win %s,Blue Win %s" % (
                    #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                    RV.data_update(wargame_town)
                    if first_episode_num % 12000 == 0 and first_episode_num != 0:
                        masac.save_model('./models_0101_4/model', first_episode_num)
                    continue
            else:
                if len(wargame_town.scenario.red_tank_2.action_history) < wargame_town.rounds:
                    wargame_town.scenario.red_tank_2.action_history.append('pass')
                    wargame_town.scenario.red_tank_2.hex_history.append((0, 0))

        # ---------RTank3--------
        if tank_3.num>0:
            if first_episode_num < episode1:
                if tank_3.co_x == 17 and tank_3.co_y == 8:
                    num3 = 5
                else:
                    temp3 = np.random.rand()
                    if temp3 < threshold1:
                        num3 = masac.choose_action(state3)
                    elif temp3 < threshold2:
                        num3 = 6
                        tank_3.change_to_fire_state()
                        tank_3.direct_fire(enemytanks[2])
                    elif temp3 < threshold3:
                        num3 = 6
                        tank_3.change_to_fire_state()
                        tank_3.direct_fire(enemytanks[3])
                    else:
                        mind = 100
                        for i in range(len(neighbours3)):
                            d = tank_3.wargame_env.game_map.get_distance_between_hex(tank_3.goal[0], tank_3.goal[1],
                                                                                     neighbours3[i][0],
                                                                                     neighbours3[i][1])
                            if d < mind:
                                mind = d
                                number = i
                        num3 = number
            else:
                if tank_3.co_x == 17 and tank_3.co_y == 8:
                    num3 = 5
                else:
                    num3 = masac.choose_action(state3)
            out3, result = replace_to_action1(wargame_town, wargame_town.scenario.red_tank_3, enemytanks, state3, num3)
            if RENDER:
                wargame_town.render()  # line:9
            state_next3 = get_state_4(wargame_town, wargame_town.scenario.red_tank_3, enemytanks)
            done = wargame_town.check_win()
            r3 = get_reward4(wargame_town, wargame_town.scenario.red_tank_3, state3, state_next3, out3, done)
            buffer_s3.append(state3)
            buffer_a3.append(num3)
            buffer_r3.append(r3)
            if done or wargame_town.rounds == MAX_STEPS:
                war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                if done:
                    v_s_3 = 0
                else:
                    v_s_3 = masac.get_v(state_next3)
                discounted_r = []
                for r3 in buffer_r3[::-1]:
                    v_s_3 = r3 + GAMMA * v_s_3
                    discounted_r.append(v_s_3)
                discounted_r.reverse()
                bs, ba, br = np.vstack(buffer_s3), np.vstack(buffer_a3), np.array(discounted_r)[:, None]
                buffer_s3, buffer_a3, buffer_r3 = [], [], []
                masac.update(np.hstack((bs, ba, br)))
                if done or wargame_town.rounds == MAX_STEPS:
                    ep_rs.append(ep_r)
                    first_episode_num += 1
                    # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                    wargame_town.rounds = 0
                    wargame_town.reset()
                    # print("First Half %s :Red Win %s,Blue Win %s" % (
                    #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                    RV.data_update(wargame_town)
                    if first_episode_num % 12000 == 0 and first_episode_num != 0:
                        masac.save_model('./models_0101_4/model', first_episode_num)
                    continue
            else:
                if len(wargame_town.scenario.red_tank_3.action_history) < wargame_town.rounds:
                    wargame_town.scenario.red_tank_3.action_history.append('pass')
                    wargame_town.scenario.red_tank_3.hex_history.append((0, 0))

        # ----------RTank4------------
        if tank_4.num>0:
            if first_episode_num < episode1:
                if tank_4.co_x == 17 and tank_4.co_y == 8:
                    num4 = 5
                else:
                    temp4 = np.random.rand()
                    if temp4 < threshold1:
                        num4 = masac.choose_action(state4)
                    elif temp4 < threshold2:
                        num4 = 6
                        tank_4.change_to_fire_state()
                        tank_4.direct_fire(enemytanks[2])
                    elif temp4 < threshold3:
                        num4 = 6
                        tank_4.change_to_fire_state()
                        tank_4.direct_fire(enemytanks[3])
                    else:
                        mind = 100
                        for i in range(len(neighbours4)):
                            d = tank_4.wargame_env.game_map.get_distance_between_hex(tank_4.goal[0], tank_4.goal[1],
                                                                                     neighbours4[i][0],
                                                                                     neighbours4[i][1])
                            if d < mind:
                                mind = d
                                number = i
                        num4 = number
            else:
                if tank_4.co_x == 17 and tank_4.co_y == 8:
                    num4 = 5
                else:
                    num4 = masac.choose_action(state4)
            out4, result = replace_to_action1(wargame_town, wargame_town.scenario.red_tank_4, enemytanks, state4, num4)
            if RENDER:
                wargame_town.render()  # line:9
            state_next4 = get_state_4(wargame_town, wargame_town.scenario.red_tank_4,
                                      enemytanks)
            done = wargame_town.check_win()
            r4 = get_reward4(wargame_town, wargame_town.scenario.red_tank_4, state4, state_next4, out4, done)
            buffer_s4.append(state4)
            buffer_a4.append(num4)
            buffer_r4.append(r4)
            if done or wargame_town.rounds == MAX_STEPS:
                war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                if done:
                    v_s_4 = 0
                else:
                    v_s_4 = masac.get_v(state_next4)
                discounted_r = []
                for r4 in buffer_r4[::-1]:
                    v_s_4 = r4 + GAMMA * v_s_4
                    discounted_r.append(v_s_4)
                discounted_r.reverse()
                bs, ba, br = np.vstack(buffer_s4), np.vstack(buffer_a4), np.array(discounted_r)[:, None]
                buffer_s4, buffer_a4, buffer_r4 = [], [], []
                masac.update(np.hstack((bs, ba, br)))
                if done or wargame_town.rounds == MAX_STEPS:
                    ep_rs.append(ep_r)
                    first_episode_num += 1
                    # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                    wargame_town.rounds = 0
                    wargame_town.reset()
                    # print("First Half %s :Red Win %s,Blue Win %s" % (
                    #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                    RV.data_update(wargame_town)
                    if first_episode_num % 12000 == 0 and first_episode_num != 0:
                        masac.save_model('./models_0101_4/model', first_episode_num)
                    continue
            else:
                if len(wargame_town.scenario.red_tank_4.action_history) < wargame_town.rounds:
                    wargame_town.scenario.red_tank_4.action_history.append('pass')
                    wargame_town.scenario.red_tank_4.hex_history.append((0, 0))

        # ---------RTank5----------
        if tank_5.num>0:
            if first_episode_num < episode1:
                if tank_5.co_x == 17 and tank_5.co_y == 8:
                    num5 = 5
                else:
                    temp_5 = np.random.rand()
                    if temp_5 < threshold1:
                        num5 = masac.choose_action(state5)
                    elif temp_5 < threshold2:
                        num5 = 6
                        tank_5.change_to_fire_state()
                        tank_5.direct_fire(enemytanks[4])
                    elif temp_5 < threshold3:
                        num5 = 6
                        tank_5.change_to_fire_state()
                        tank_5.direct_fire(enemytanks[5])
                    else:
                        mind = 100
                        for i in range(len(neighbours5)):
                            d = tank_5.wargame_env.game_map.get_distance_between_hex(tank_5.goal[0], tank_5.goal[1],
                                                                                     neighbours5[i][0],
                                                                                     neighbours5[i][1])
                            if d < mind:
                                mind = d
                                number = i
                        num5 = number

            else:
                if tank_5.co_x == 17 and tank_5.co_y == 8:
                    num5 = 5
                else:
                    num5 = masac.choose_action(state5)
            out5, result = replace_to_action1(wargame_town, wargame_town.scenario.red_tank_5, enemytanks, state5, num5)
            if RENDER:
                wargame_town.render()  # line:95
            state_next5 = get_state_4(wargame_town, wargame_town.scenario.red_tank_5, enemytanks)
            done = wargame_town.check_win()
            r5 = get_reward4(wargame_town, wargame_town.scenario.red_tank_5, state5, state_next5, out5, done)
            buffer_s5.append(state5)
            buffer_a5.append(num5)
            buffer_r5.append(r5)
            if done or wargame_town.rounds == MAX_STEPS:
                war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                if done:
                    v_s_5 = 0
                else:
                    v_s_5 = masac.get_v(state_next5)
                discounted_r = []
                for r5 in buffer_r5[::-1]:
                    v_s_5 = r5 + GAMMA * v_s_5
                    discounted_r.append(v_s_5)
                discounted_r.reverse()
                bs, ba, br = np.vstack(buffer_s5), np.vstack(buffer_a5), np.array(discounted_r)[:, None]
                buffer_s5, buffer_a5, buffer_r5 = [], [], []
                masac.update(np.hstack((bs, ba, br)))
                if done or wargame_town.rounds == MAX_STEPS:
                    ep_rs.append(ep_r)
                    first_episode_num += 1
                    # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                    wargame_town.rounds = 0
                    wargame_town.reset()
                    # print("First Half %s :Red Win %s,Blue Win %s" % (
                    #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                    RV.data_update(wargame_town)
                    if first_episode_num % 12000 == 0 and first_episode_num != 0:
                        masac.save_model('./models_0101_4/model', first_episode_num)
                    continue
            else:
                if len(wargame_town.scenario.red_tank_5.action_history) < wargame_town.rounds:
                    wargame_town.scenario.red_tank_5.action_history.append('pass')
                    wargame_town.scenario.red_tank_5.hex_history.append((0, 0))

        # ------RTank6------
        if tank_6.num>0:
            if first_episode_num < episode1:
                if tank_6.co_x == 17 and tank_6.co_y == 8:
                    num6 = 5
                else:
                    temp_6 = np.random.rand()
                    if temp_6 < threshold1:
                        num6 = masac.choose_action(state6)
                    elif temp_6 < threshold2:
                        num6 = 6
                        tank_6.change_to_fire_state()
                        tank_6.direct_fire(enemytanks[4])
                    elif temp_6 < threshold3:
                        num6 = 6
                        tank_6.change_to_fire_state()
                        tank_6.direct_fire(enemytanks[5])
                    else:
                        mind = 100
                        for i in range(len(neighbours6)):
                            d = tank_6.wargame_env.game_map.get_distance_between_hex(tank_6.goal[0], tank_6.goal[1],
                                                                                     neighbours6[i][0],
                                                                                     neighbours6[i][1])
                            if d < mind:
                                mind = d
                                number = i
                        num6 = number

            else:
                if tank_6.co_x == 17 and tank_6.co_y == 8:
                    num6 = 5
                else:
                    num6 = masac.choose_action(state6)
            out6, result = replace_to_action1(wargame_town, wargame_town.scenario.red_tank_6, enemytanks, state6, num6)
            if RENDER:
                wargame_town.render()  # line:95
            state_next6 = get_state_4(wargame_town, wargame_town.scenario.red_tank_6, enemytanks)
            done = wargame_town.check_win()
            r6 = get_reward4(wargame_town, wargame_town.scenario.red_tank_6, state6, state_next6, out6, done)
            buffer_s6.append(state6)
            buffer_a6.append(num6)
            buffer_r6.append(r6)
            if done or wargame_town.rounds == MAX_STEPS:
                war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                if done:
                    v_s_6 = 0
                else:
                    v_s_6 = masac.get_v(state_next6)
                discounted_r = []
                for r6 in buffer_r6[::-1]:
                    v_s_6 = r6 + GAMMA * v_s_6
                    discounted_r.append(v_s_6)
                discounted_r.reverse()
                bs, ba, br = np.vstack(buffer_s6), np.vstack(buffer_a6), np.array(discounted_r)[:, None]
                buffer_s6, buffer_a6, buffer_r6 = [], [], []
                masac.update(np.hstack((bs, ba, br)))
                if done or wargame_town.rounds == MAX_STEPS:
                    ep_rs.append(ep_r)
                    first_episode_num += 1
                    # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                    wargame_town.rounds = 0
                    wargame_town.reset()
                    # print("First Half %s :Red Win %s,Blue Win %s" % (
                    #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                    RV.data_update(wargame_town)
                    if first_episode_num % 12000 == 0 and first_episode_num != 0:
                        masac.save_model('./models_0101_4/model', first_episode_num)
                    continue
            else:
                if len(wargame_town.scenario.red_tank_6.action_history) < wargame_town.rounds:
                    wargame_town.scenario.red_tank_6.action_history.append('pass')
                    wargame_town.scenario.red_tank_6.hex_history.append((0, 0))


        # ---------RTank7----------
        if tank_7.num>0:
            if first_episode_num < episode1:
                if tank_7.co_x == 16 and tank_7.co_y == 7:
                    num7 = 5
                else:
                    temp7 = np.random.rand()
                    if temp7 < threshold1:
                        num7 = masac.choose_action(state7)
                    elif temp7 < threshold2:
                        num7 = 6
                        tank_7.change_to_fire_state()
                        tank_7.direct_fire(enemytanks[6])
                    elif temp7 < threshold3:
                        num7 = 6
                        tank_7.change_to_fire_state()
                        tank_7.direct_fire(enemytanks[7])
                    else:
                        mind = 100
                        for i in range(len(neighbours7)):
                            d = tank_7.wargame_env.game_map.get_distance_between_hex(tank_7.goal[0], tank_7.goal[1],
                                                                                     neighbours7[i][0],
                                                                                     neighbours7[i][1])
                            if d < mind:
                                mind = d
                                number = i
                        num7 = number
                        # num = r2_road(tank_1.co_x, tank_1.co_y
            else:
                if tank_7.co_x == 18 and tank_7.co_y == 12:
                    num7 = 5
                else:
                    num7 = masac.choose_action(state7)
            out7, result = replace_to_action1(wargame_town, wargame_town.scenario.red_tank_7, enemytanks, state7, num7)
            if RENDER:
                wargame_town.render()  # line:95
            state_next7 = get_state_4(wargame_town, wargame_town.scenario.red_tank_7,
                                      enemytanks)
            done = wargame_town.check_win()
            r7 = get_reward4(wargame_town, wargame_town.scenario.red_tank_7, state7, state_next7, out7, done)
            buffer_s7.append(state7)
            buffer_a7.append(num7)
            buffer_r7.append(r7)
            if done or wargame_town.rounds == MAX_STEPS:
                war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                if done:
                    v_s_7 = 0
                else:
                    v_s_7 = masac.get_v(state_next5)
                discounted_r = []
                for r7 in buffer_r7[::-1]:
                    v_s_7 = r5 + GAMMA * v_s_7
                    discounted_r.append(v_s_7)
                discounted_r.reverse()
                bs, ba, br = np.vstack(buffer_s7), np.vstack(buffer_a7), np.array(discounted_r)[:, None]
                buffer_s7, buffer_a7, buffer_r7 = [], [], []
                masac.update(np.hstack((bs, ba, br)))
                if done or wargame_town.rounds == MAX_STEPS:
                    ep_rs.append(ep_r)
                    first_episode_num += 1
                    # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                    wargame_town.rounds = 0
                    wargame_town.reset()
                    # print("First Half %s :Red Win %s,Blue Win %s" % (
                    #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                    RV.data_update(wargame_town)
                    if first_episode_num % 12000 == 0 and first_episode_num != 0:
                        masac.save_model('./models_0101_4/model', first_episode_num)
                    continue
            else:
                if len(wargame_town.scenario.red_tank_7.action_history) < wargame_town.rounds:
                    wargame_town.scenario.red_tank_7.action_history.append('pass')
                    wargame_town.scenario.red_tank_7.hex_history.append((0, 0))

        # ------RTank8------
        if tank_8.num>0:
            if first_episode_num < episode1:
                if tank_8.co_x == 16 and tank_8.co_y == 8:
                    num8 = 5
                else:
                    temp8 = np.random.rand()
                    if temp8 < threshold1:
                        num8 = masac.choose_action(state8)
                    elif temp8 < threshold2:
                        num8 = 6
                        tank_8.change_to_fire_state()
                        tank_8.direct_fire(enemytanks[6])
                    elif temp8 < threshold3:
                        num8 = 6
                        tank_8.change_to_fire_state()
                        tank_8.direct_fire(enemytanks[7])
                    else:
                        mind = 100
                        for i in range(len(neighbours8)):
                            d = tank_8.wargame_env.game_map.get_distance_between_hex(tank_8.goal[0], tank_8.goal[1],
                                                                                     neighbours8[i][0],
                                                                                     neighbours8[i][1])
                            if d < mind:
                                mind = d
                                number = i
                        num8 = number
                        # num = r2_road(tank_1.co_x, tank_1.co_y
            else:
                if tank_8.co_x == 18 and tank_8.co_y == 12:
                    num8 = 5
                else:
                    num8 = masac.choose_action(state8)

            out8, result = replace_to_action1(wargame_town, wargame_town.scenario.red_tank_8, enemytanks, state8, num8)
            if RENDER:
                wargame_town.render()  # line:95
            state_next8 = get_state_4(wargame_town, wargame_town.scenario.red_tank_8, enemytanks)
            done = wargame_town.check_win()
            r8 = get_reward4(wargame_town, wargame_town.scenario.red_tank_8, state8, state_next8, out8, done)
            buffer_s8.append(state8)
            buffer_a8.append(num8)
            buffer_r8.append(r8)
            if done or wargame_town.rounds == MAX_STEPS:
                war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                if done:
                    v_s_8 = 0
                else:
                    v_s_8 = masac.get_v(state_next5)
                discounted_r = []
                for r8 in buffer_r8[::-1]:
                    v_s_8 = r5 + GAMMA * v_s_8
                    discounted_r.append(v_s_8)
                discounted_r.reverse()
                bs, ba, br = np.vstack(buffer_s8), np.vstack(buffer_a8), np.array(discounted_r)[:, None]
                buffer_s8, buffer_a8, buffer_r8 = [], [], []
                masac.update(np.hstack((bs, ba, br)))
                if done or wargame_town.rounds == MAX_STEPS:
                    ep_rs.append(ep_r)
                    first_episode_num += 1
                    # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                    wargame_town.rounds = 0
                    wargame_town.reset()
                    # print("First Half %s :Red Win %s,Blue Win %s" % (
                    #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                    RV.data_update(wargame_town)
                    if first_episode_num % 12000 == 0 and first_episode_num != 0:
                        masac.save_model('./models_0101_4/model', first_episode_num)
                    continue
            else:

                if len(wargame_town.scenario.red_tank_8.action_history) < wargame_town.rounds:
                    wargame_town.scenario.red_tank_8.action_history.append('pass')
                    wargame_town.scenario.red_tank_8.hex_history.append((0, 0))

        # ---------RPlane9----------
        if tank_9.num>0:
            if UAV_list[0] == 1 and wargame_town.rounds >= 0 and RPlane9_exist >= 0.5:
                if first_episode_num < episode1:
                    if tank_9.co_x == 16 and tank_9.co_y == 4:
                        num9 = 1
                    else:
                        temp9 = np.random.rand()
                        if temp9 < threshold1:
                            num9 = masac.choose_action(state9)
                        elif temp9 < threshold2:
                            num9 = 6
                            tank_9.change_to_fire_state()
                            tank_9.direct_fire(enemytanks[8])
                        elif temp9 < threshold3:
                            num9 = 6
                            tank_9.change_to_fire_state()
                            tank_9.direct_fire(enemytanks[9])
                        else:
                            mind = 100
                            for i in range(len(neighbours9)):
                                d = tank_9.wargame_env.game_map.get_distance_between_hex(tank_9.goal[0], tank_9.goal[1],
                                                                                         neighbours9[i][0],
                                                                                         neighbours9[i][1])
                                if d < mind:
                                    mind = d
                                    number = i
                            num9 = number
                else:
                    if tank_9.co_x == 16 and tank_9.co_y == 4:
                        num9 = 1
                    else:
                        num9 = masac.choose_action(state9)
                out9, result = replace_to_action1(wargame_town, wargame_town.scenario.red_plane_9, enemytanks, state9,
                                                  num9)
                if RENDER:
                    wargame_town.render()  # line:95
                state_next9 = get_state_4(wargame_town, wargame_town.scenario.red_plane_9, enemytanks)
                done = wargame_town.check_win()
                r9 = get_reward4(wargame_town, wargame_town.scenario.red_plane_9, state9, state_next9, out9, done)
                buffer_s9.append(state9)
                buffer_a9.append(num9)
                buffer_r9.append(r9)
                if done or wargame_town.rounds == MAX_STEPS:
                    war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                    if done:
                        v_s_9 = 0
                    else:
                        v_s_9 = masac.get_v(state_next9)
                    discounted_r = []
                    for r9 in buffer_r9[::-1]:
                        v_s_9 = r9 + GAMMA * v_s_9
                        discounted_r.append(v_s_9)
                    discounted_r.reverse()
                    bs, ba, br = np.vstack(buffer_s9), np.vstack(buffer_a9), np.array(discounted_r)[:, None]
                    buffer_s9, buffer_a9, buffer_r9 = [], [], []
                    masac.update(np.hstack((bs, ba, br)))
                    if done or wargame_town.rounds == MAX_STEPS:
                        ep_rs.append(ep_r)
                        first_episode_num += 1
                        # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                        wargame_town.rounds = 0
                        wargame_town.reset()
                        # print("First Half %s :Red Win %s,Blue Win %s" % (
                        #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                        RV.data_update(wargame_town)
                        if first_episode_num % 12000 == 0 and first_episode_num != 0:
                            masac.save_model('./models_0101_4/model', first_episode_num)
                        continue
                else:
                    if len(wargame_town.scenario.red_plane_9.action_history) < wargame_town.rounds:
                        wargame_town.scenario.red_plane_9.action_history.append('pass')
                        wargame_town.scenario.red_plane_9.hex_history.append((0, 0))
            else:
                pass

        # ------RPlane10------
        if tank_10.num > 0:
            if UAV_list[1] == 1 and wargame_town.rounds >= 10 and RPlane10_exist >= 0.5:
                if first_episode_num < episode1:
                    if tank_10.co_x == 17 and tank_10.co_y == 4:
                        num10 = 5
                    else:
                        temp10 = np.random.rand()
                        if temp10 < threshold1:
                            num10 = masac.choose_action(state10)
                        elif temp10 < threshold2:
                            num10 = 6
                            tank_10.change_to_fire_state()
                            tank_10.direct_fire(enemytanks[8])
                        elif temp10 < threshold3:
                            num10 = 6
                            tank_10.change_to_fire_state()
                            tank_10.direct_fire(enemytanks[9])
                        else:
                            mind = 100
                            for i in range(len(neighbours10)):
                                d = tank_10.wargame_env.game_map.get_distance_between_hex(tank_10.goal[0],
                                                                                          tank_10.goal[1],
                                                                                          neighbours10[i][0],
                                                                                          neighbours10[i][1])
                                if d < mind:
                                    mind = d
                                    number = i
                            num10 = number
                else:
                    if tank_10.co_x == 17 and tank_10.co_y == 4:
                        num10 = 5
                    else:
                        num10 = masac.choose_action(state10)
                out10, result = replace_to_action1(wargame_town, wargame_town.scenario.red_plane_10, enemytanks,
                                                   state10, num10)
                if RENDER:
                    wargame_town.render()  # line:95
                state_next10 = get_state_4(wargame_town, wargame_town.scenario.red_plane_10, enemytanks)
                done = wargame_town.check_win()
                r10 = get_reward4(wargame_town, wargame_town.scenario.red_plane_10, state10, state_next10, out10, done)
                buffer_s10.append(state10)
                buffer_a10.append(num10)
                buffer_r10.append(r10)
                r = r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9 + r10
                # 下面进行更新算法
                ep_r += r
                if done or wargame_town.rounds == MAX_STEPS:
                    war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                    if done:
                        v_s_10 = 0
                    else:
                        v_s_10 = masac.get_v(state_next10)
                    discounted_r = []
                    for r10 in buffer_r10[::-1]:
                        v_s_10 = r10 + GAMMA * v_s_10
                        discounted_r.append(v_s_10)
                    discounted_r.reverse()
                    bs, ba, br = np.vstack(buffer_s10), np.vstack(buffer_a10), np.array(discounted_r)[:, None]
                    buffer_s10, buffer_a10, buffer_r10 = [], [], []
                    masac.update(np.hstack((bs, ba, br)))
                    if done or wargame_town.rounds == MAX_STEPS:
                        ep_rs.append(ep_r)
                        first_episode_num += 1
                        # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                        wargame_town.rounds = 0
                        wargame_town.reset()
                        # print("First Half %s :Red Win %s,Blue Win %s" % (
                        #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                        RV.data_update(wargame_town)
                        if first_episode_num % 12000 == 0 and first_episode_num != 0:
                            masac.save_model('./models_0101_4/model', first_episode_num)
                        continue
                else:
                    if len(wargame_town.scenario.red_plane_10.action_history) < wargame_town.rounds:
                        wargame_town.scenario.red_plane_10.action_history.append('pass')
                        wargame_town.scenario.red_plane_10.hex_history.append((0, 0))
            else:
                pass

        # ------RPlane11------
        if UAV_list[2] == 1 and wargame_town.rounds >= 20 and RPlane11_exist >= 0.5:
            if first_episode_num < episode1:
                if tank_11.co_x == 18 and tank_11.co_y == 4:
                    num11 = 1
                else:
                    temp11 = np.random.rand()
                    if temp11 < threshold1:
                        num11 = masac.choose_action(state11)
                    elif temp11 < threshold2:
                        num11 = 6
                        tank_11.change_to_fire_state()
                        tank_11.direct_fire(enemytanks[8])
                    elif temp11 < threshold3:
                        num11 = 6
                        tank_11.change_to_fire_state()
                        tank_11.direct_fire(enemytanks[9])
                    else:
                        mind = 100
                        for i in range(len(neighbours11)):
                            d = tank_11.wargame_env.game_map.get_distance_between_hex(tank_11.goal[0], tank_11.goal[1],
                                                                                      neighbours11[i][0], neighbours11[i][1])

                            if d < mind:
                                mind = d
                                number = 1
                        num11 = number

            else:
                if tank_11.co_x == 18 and tank_11.co_y == 4:
                    num11 = 1
                else:
                    num11 = masac.choose_action(state11)
            out11, result = replace_to_action1(wargame_town, wargame_town.scenario.red_plane_11, enemytanks, state11, num11)
            if RENDER:
                wargame_town.render()
            state_next11 = get_state_4(wargame_town, wargame_town.scenario.red_plane_11, enemytanks)
            done = wargame_town.check_win()
            r11 = get_reward4(wargame_town, wargame_town.scenario.red_plane_11, state11, state_next11, out11, done)
            buffer_s11.append(state11)
            buffer_a11.append(num11)
            buffer_r11.append(r11)
            if done or wargame_town.rounds == MAX_STEPS:
                war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                if done:
                    v_s_11 = 0
                else:
                    v_s_11 = masac.get_v(state_next11)
                discounted_r = []
                for r11 in buffer_r11[::-1]:
                    v_s_11 = r11 + GAMMA * v_s_11
                    discounted_r.append(v_s_11)
                discounted_r.reverse()
                bs, ba, br = np.vstack(buffer_s11), np.vstack(buffer_a11), np.array(discounted_r)[:, None]
                buffer_s11, buffer_a11, buffer_r11 = [], [], []
                masac.update(np.hstack((bs, ba, br)))
                if done or wargame_town.rounds == MAX_STEPS:
                    ep_rs.append(ep_r)
                    first_episode_num += 1
                    # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                    wargame_town.rounds = 0
                    wargame_town.reset()
                    # print("First Half %s :Red Win %s,Blue Win %s" % (
                    #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                    RV.data_update(wargame_town)
                    if first_episode_num % 12000 == 0 and first_episode_num != 0:
                        masac.save_model('./models_0101_4/model', first_episode_num)
                    continue
            else:
                if len(wargame_town.scenario.red_plane_11.action_history) < wargame_town.rounds:
                    wargame_town.scenario.red_plane_11.action_history.append('pass')
                    wargame_town.scenario.red_plane_11.hex_history.append((0, 0))
        else:
            pass

        # ------RPlane12------
        if UAV_list[3] == 1 and wargame_town.rounds >= 30 and RPlane12_exist >= 0.5:
            if first_episode_num < episode1:
                if tank_12.co_x == 19 and tank_12.co_y == 4:
                    num12 = 1
                else:
                    temp12 = np.random.rand()
                    if temp12 < threshold1:
                        num12 = masac.choose_action(state12)
                    elif temp12 < threshold2:
                        num12 = 6
                        tank_12.change_to_fire_state()
                        tank_12.direct_fire(enemytanks[8])
                    elif temp12 < threshold3:
                        num12 = 6
                        tank_12.change_to_fire_state()
                        tank_12.direct_fire(enemytanks[9])
                    else:
                        mind = 100
                        for i in range(len(neighbours12)):
                            d = tank_12.wargame_env.game_map.get_distance_between_hex(tank_12.goal[0],
                                                                                      tank_12.goal[1],
                                                                                      neighbours12[i][0],
                                                                                      neighbours12[i][1])
                            if d < mind:
                                mind = d
                                number = 1
                        num12 = number
            else:
                if tank_12.co_x == 19 and tank_12.co_y == 4:
                    num12 = 1
                else:
                    num12 = masac.choose_action(state12)
            out12, result = replace_to_action1(wargame_town, wargame_town.scenario.red_plane_12, enemytanks, state12, num12)
            if RENDER:
                wargame_town.render()
            state_next12 = get_state_4(wargame_town, wargame_town.scenario.red_plane_12, enemytanks)
            done = wargame_town.check_win()
            r12 = get_reward4(wargame_town, wargame_town.scenario.red_plane_12, state12, state_next12, out12, done)
            buffer_s12.append(state12)
            buffer_a12.append(num12)
            buffer_r12.append(r12)
            if done or wargame_town.rounds == MAX_STEPS:
                war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
                if done:
                    v_s_12 = 0
                else:
                    v_s_12 = masac.get_v(state_next12)
                discounted_r = []
                for r12 in buffer_r12[::-1]:
                    v_s_12 = r12 + GAMMA * v_s_12
                    discounted_r.append(v_s_12)
                discounted_r.reverse()
                bs, ba, br = np.vstack(buffer_s12), np.vstack(buffer_a12), np.array(discounted_r)[:, None]
                buffer_s12, buffer_a12, buffer_r12 = [], [], []
                masac.update(np.hstack((bs, ba, br)))
                if done or wargame_town.rounds == MAX_STEPS:
                    ep_rs.append(ep_r)
                    first_episode_num += 1
                    # print('episode:%d,reward:%f，rounds:%d' % (first_episode_num, ep_r, wargame_town.rounds))
                    wargame_town.rounds = 0
                    wargame_town.reset()
                    # print("First Half %s :Red Win %s,Blue Win %s" % (
                    #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                    RV.data_update(wargame_town)
                    if first_episode_num % 12000 == 0 and first_episode_num != 0:
                        masac.save_model('./models_0101_4/model', first_episode_num)
                    continue
            else:
                if len(wargame_town.scenario.red_plane_12.action_history) < wargame_town.rounds:
                    wargame_town.scenario.red_plane_12.action_history.append('pass')
                    wargame_town.scenario.red_plane_12.hex_history.append((0, 0))
        else:
            pass

        wargame_town.check_indirect_fire('blue')
        # 红蓝方行动开关设置
        wargame_town.scenario.red_tank_1.done = True
        wargame_town.scenario.red_tank_2.done = True
        wargame_town.scenario.red_tank_3.done = True
        wargame_town.scenario.red_tank_4.done = True
        wargame_town.scenario.red_tank_5.done = True
        wargame_town.scenario.red_tank_6.done = True
        wargame_town.scenario.red_tank_7.done = True
        wargame_town.scenario.red_tank_8.done = True

        if UAV_list[0] == 1:
            wargame_town.scenario.red_plane_9.done = True
        else:
            pass

        if UAV_list[1] == 1:
            wargame_town.scenario.red_plane_10.done = True
        else:
            pass

        if UAV_list[2] == 1:
            wargame_town.scenario.red_plane_11.done = True
        else:
            pass

        if UAV_list[3] == 1:
            wargame_town.scenario.red_plane_12.done = True
        else:
            pass

        wargame_town.scenario.blue_tank_1.done = False
        wargame_town.scenario.blue_tank_2.done = False
        wargame_town.scenario.blue_tank_3.done = False
        wargame_town.scenario.blue_tank_4.done = False
        wargame_town.scenario.blue_tank_5.done = False
        wargame_town.scenario.blue_tank_6.done = False
        wargame_town.scenario.blue_tank_7.done = False
        wargame_town.scenario.blue_tank_8.done = False
        wargame_town.scenario.blue_tank_9.done = False
        wargame_town.scenario.blue_tank_10.done = False
        player_2.blue_choose_action(wargame_town)
        # 判断是否取胜，重置
        if RENDER:
            wargame_town.render()
        done = wargame_town.check_win()
        if done:
            war_result.append(wargame_town.red_win_times - wargame_town.blue_win_times)
            first_episode_num += 1
            wargame_town.rounds = 0
            wargame_town.reset()
            # print("First Half %s :Red Win %s,Blue Win %s" % (
            #     first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
            RV.data_update(wargame_town)
        else:
            if len(wargame_town.scenario.blue_tank_1.action_history) < wargame_town.rounds:
                wargame_town.scenario.blue_tank_1.action_history.append('pass')
                wargame_town.scenario.blue_tank_1.hex_history.append((0, 0))
            if len(wargame_town.scenario.blue_tank_2.action_history) < wargame_town.rounds:
                wargame_town.scenario.blue_tank_2.action_history.append('pass')
                wargame_town.scenario.blue_tank_2.hex_history.append((0, 0))
            if len(wargame_town.scenario.blue_tank_3.action_history) < wargame_town.rounds:
                wargame_town.scenario.blue_tank_3.action_history.append('pass')
                wargame_town.scenario.blue_tank_3.hex_history.append((0, 0))
            if len(wargame_town.scenario.blue_tank_4.action_history) < wargame_town.rounds:
                wargame_town.scenario.blue_tank_4.action_history.append('pass')
                wargame_town.scenario.blue_tank_4.hex_history.append((0, 0))

    # 输出算子数据到excel:'test00.xlsx'
        # wargame_data = {"episode": episode_num,
        #                 'timestep': timestep_list,
        #                 'goal_point': goal_point_list,
        #                 'R1_height': R1_gaochenglist,
        #                 'R1_state': R1_statelist,
        #                 'R1_position': R1_positionlist,
        #                 'R2_height': R2_gaochenglist,
        #                 'R2_state': R2_statelist,
        #                 'R2_position': R2_positionlist,
        #                 'R3_height': R3_gaochenglist,
        #                 'R3_state': R3_statelist,
        #                 'R3_position': R3_positionlist,
        #                 'R4_height': R4_gaochenglist,
        #                 'R4_state': R4_statelist,
        #                 'R4_position': R4_positionlist,
        #                 'R5_height': R5_gaochenglist,
        #                 'R5_state': R5_statelist,
        #                 'R5_position': R5_positionlist,
        #                 'R6_height': R6_gaochenglist,
        #                 'R6_state': R6_statelist,
        #                 'R6_position': R6_positionlist,
        #                 'R7_height': R7_gaochenglist,
        #                 'R7_state': R7_statelist,
        #                 'R7_position': R7_positionlist,
        #                 'R8_height': R8_gaochenglist,
        #                 'R8_state': R8_statelist,
        #                 'R8_position': R8_positionlist,
        #                 'R9_height': R9_gaochenglist,
        #                 'R9_state': R9_statelist,
        #                 'R9_position': R9_positionlist,
        #                 'R10_height': R10_gaochenglist,
        #                 'R10_state': R10_statelist,
        #                 'R10_position': R10_positionlist,
        #                 'B1_height': B1_gaochenglist,
        #                 'B1_state': B1_statelist,
        #                 'B1_position': B1_positionlist,
        #                 'B2_height': B2_gaochenglist,
        #                 'B2_state': B2_statelist,
        #                 'B2_position': B2_positionlist,
        #                 'B3_height': B3_gaochenglist,
        #                 'B3_state': B3_statelist,
        #                 'B3_position': B3_positionlist,
        #                 'B4_height': B4_gaochenglist,
        #                 'B4_state': B4_statelist,
        #                 'B4_position': B4_positionlist,
        #                 'B5_height': B5_gaochenglist,
        #                 'B5_state': B5_statelist,
        #                 'B5_position': B5_positionlist,
        #                 'B6_height': B6_gaochenglist,
        #                 'B6_state': B6_statelist,
        #                 'B6_position': B6_positionlist,
        #                 'B7_height': B7_gaochenglist,
        #                 'B7_state': B7_statelist,
        #                 'B7_position': B7_positionlist,
        #                 'B8_height': B8_gaochenglist,
        #                 'B8_state': B8_statelist,
        #                 'B8_position': B8_positionlist,
        #                 'B9_height': B1_gaochenglist,
        #                 'B9_state': B9_statelist,
        #                 'B9_position': B9_positionlist,
        #                 'B10_height': B10_gaochenglist,
        #                 'B10_state': B10_statelist,
        #                 'B10_position': B10_positionlist,
        #                 }
        # df = pd.DataFrame(wargame_data)
        # df.to_excel('test00.xlsx', index=False)


    # 输出算子数据到Excel_'测试2.xlsx'
    wargame_info = {'episode_num': episode_num,
                    'wargame_town_steps': timestep_list,

                    'R1_height': R1_gaochenglist,
                    'R1_position': R1_positionlist,
                    'R1_obj_distance': R1_to_obj_distancelist,
                    'R1_speed': R1_speedlist,
                    'R1_attacklist': R1_attacklist,
                    'R1_deflist': R1_deflist,

                    'R2_height': R2_gaochenglist,
                    'R2_position': R2_positionlist,
                    'R2_obj_distance': R2_to_obj_distancelist,
                    'R2_speed': R2_speedlist,
                    'R2_attacklist': R2_attacklist,
                    'R2_deflist': R2_deflist,

                    'R3_height': R3_gaochenglist,
                    'R3_position': R3_positionlist,
                    'R3_obj_distance': R3_to_obj_distancelist,
                    'R3_speed': R1_speedlist,
                    'R3_attacklist': R3_attacklist,
                    'R3_deflist': R3_deflist,

                    'R4_height': R4_gaochenglist,
                    'R4_position': R4_positionlist,
                    'R4_obj_distance': R4_to_obj_distancelist,
                    'R4_speed': R4_speedlist,
                    'R4_attacklist': R4_attacklist,
                    'R4_deflist': R4_deflist,

                    'R5_height': R5_gaochenglist,
                    'R5_position': R5_positionlist,
                    'R5_obj_distance': R5_to_obj_distancelist,
                    'R5_speed': R5_speedlist,
                    'R5_attacklist': R5_attacklist,
                    'R5_deflist': R5_deflist,

                    'R6_height': R6_gaochenglist,
                    'R6_position': R6_positionlist,
                    'R6_obj_distance': R6_to_obj_distancelist,
                    'R6_speed': R6_speedlist,
                    'R6_attacklist': R6_attacklist,
                    'R6_deflist': R6_deflist,

                    'R7_height': R7_gaochenglist,
                    'R7_position': R7_positionlist,
                    'R7_obj_distance': R7_to_obj_distancelist,
                    'R7_speed': R7_speedlist,
                    'R7_attacklist': R7_attacklist,
                    'R7_deflist': R7_deflist,

                    'R8_height': R8_gaochenglist,
                    'R8_position': R8_positionlist,
                    'R8_obj_distance': R8_to_obj_distancelist,
                    'R8_speed': R8_speedlist,
                    'R8_attacklist': R8_attacklist,
                    'R8_deflist': R8_deflist,

                    'R9_height': R9_gaochenglist,
                    'R9_position': R9_positionlist,
                    'R9_obj_distance': R9_to_obj_distancelist,
                    'R9_speed': R9_speedlist,
                    'R9_attacklist': R9_attacklist,
                    'R9_deflist': R9_deflist,

                    'R10_height': R10_gaochenglist,
                    'R10_position': R10_positionlist,
                    'R10_obj_distance': R10_to_obj_distancelist,
                    'R10_speed': R10_speedlist,
                    'R10_attacklist': R10_attacklist,
                    'R10_deflist': R10_deflist,

                    'B1_height': B1_gaochenglist,
                    'B1_position': B1_positionlist,
                    'B1_obj_distance': B1_to_obj_distancelist,
                    'B1_speed': B1_speedlist,
                    'B1_attacklist': B1_attacklist,
                    'B1_deflist': B1_deflist,

                    'B2_height': B2_gaochenglist,
                    'B2_position': B2_positionlist,
                    'B2_obj_distance': B2_to_obj_distancelist,
                    'B2_speed': B2_speedlist,
                    'B2_attacklist': B2_attacklist,
                    'B2_deflist': B2_deflist,

                    'B3_height': B3_gaochenglist,
                    'B3_position': B3_positionlist,
                    'B3_obj_distance': B3_to_obj_distancelist,
                    'B3_speed': B3_speedlist,
                    'B3_attacklist': B3_attacklist,
                    'B3_deflist': B3_deflist,

                    'B4_height': B4_gaochenglist,
                    'B4_position': B4_positionlist,
                    'B4_obj_distance': B4_to_obj_distancelist,
                    'B4_speed': B4_speedlist,
                    'B4_attacklist': B4_attacklist,
                    'B4_deflist': B4_deflist,

                    'B5_height': B5_gaochenglist,
                    'B5_position': B5_positionlist,
                    'B5_obj_distance': B5_to_obj_distancelist,
                    'B5_speed': B5_speedlist,
                    'B5_attacklist': B5_attacklist,
                    'B5_deflist': B5_deflist,

                    'B6_height': B6_gaochenglist,
                    'B6_position': B6_positionlist,
                    'B6_obj_distance': B6_to_obj_distancelist,
                    'B6_speed': B6_speedlist,
                    'B6_attacklist': B6_attacklist,
                    'B6_deflist': B6_deflist,

                    'B7_height': B7_gaochenglist,
                    'B7_position': B7_positionlist,
                    'B7_obj_distance': B7_to_obj_distancelist,
                    'B7_speed': B7_speedlist,
                    'B7_attacklist': B7_attacklist,
                    'B7_deflist': B7_deflist,

                    'B8_height': B8_gaochenglist,
                    'B8_position': B8_positionlist,
                    'B8_obj_distance': B8_to_obj_distancelist,
                    'B8_speed': B8_speedlist,
                    'B8_attacklist': B8_attacklist,
                    'B8_deflist': B8_deflist,

                    'B9_height': B9_gaochenglist,
                    'B9_position': B9_positionlist,
                    'B9_obj_distance': B9_to_obj_distancelist,
                    'B9_speed': B9_speedlist,
                    'B9_attacklist': B9_attacklist,
                    'B9_deflist': B9_deflist,

                    'B10_height': B10_gaochenglist,
                    'B10_position': B10_positionlist,
                    'B10_obj_distance': B10_to_obj_distancelist,
                    'B10_speed': B10_speedlist,
                    'B10_attacklist': B10_attacklist,
                    'B10_deflist': B10_deflist,

                    }
    wargame_result = {
        'episode_num': list(set(episode_num)),
        'war_result': war_result,
    }
    df = pd.DataFrame(wargame_info)
    df.to_csv('data/wargame_info.csv', index=False)
    df2 = pd.DataFrame(wargame_result)
    df2.to_csv('data/wargame_result.csv', index=False)
    RV.output()
    print('First End')
    # --------------------上半场所对抗结束，下半场所开始-------------------------------------------------------------------
    wargame_town.change_half()
    first_record_score(wargame_town)
    wargame_town.hud.show_break_popup = True
    wargame_town.hud.show_break()
    wargame_town.rounds = 0
    while second_episode_num <= second_half_episodes:
        if RENDER:
            wargame_town.render()
        wargame_town.rounds += 1
        print("Second Half,episode:%s, Round:%s" % (second_episode_num, wargame_town.rounds))
        wargame_town.scenario.red_tank_1.state_history.append(
            wargame_town.scenario.red_tank_1.get_piece_state())
        wargame_town.scenario.red_tank_2.state_history.append(
            wargame_town.scenario.red_tank_2.get_piece_state())
        wargame_town.scenario.blue_tank_1.state_history.append(
            wargame_town.scenario.blue_tank_1.get_piece_state())
        wargame_town.scenario.blue_tank_2.state_history.append(
            wargame_town.scenario.blue_tank_2.get_piece_state())
        wargame_town.check_indirect_fire('red')
        wargame_town.scenario.red_tank_1.done = False
        wargame_town.scenario.red_tank_2.done = False
        red_observation = player_4.red_choose_action(wargame_town)
        wargame_town.check_indirect_fire('red')
        red_observation_, red_reward, red_done = player_2.red_choose_action(wargame_town)
        if RENDER:
            wargame_town.render()
        if wargame_town.check_win():
            second_episode_num += 1
            wargame_town.reset()
            print("Second Half %s :Red Win %s,Blue Win %s" % (
                second_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
            RV.data_update(wargame_town)
        else:
            wargame_town.scenario.red_tank_1.done = False
            wargame_town.scenario.red_tank_2.done = False
            wargame_town.scenario.blue_tank_1.done = True
            wargame_town.scenario.blue_tank_2.done = True
            if len(wargame_town.scenario.red_tank_1.action_history) < wargame_town.rounds:
                wargame_town.scenario.red_tank_1.action_history.append('pass')
                wargame_town.scenario.red_tank_1.hex_history.append((0, 0))
            if len(wargame_town.scenario.red_tank_2.action_history) < wargame_town.rounds:
                wargame_town.scenario.red_tank_2.action_history.append('pass')
                wargame_town.scenario.red_tank_2.hex_history.append((0, 0))
            wargame_town.check_indirect_fire('blue')
            wargame_town.scenario.blue_tank_1.done = False
            wargame_town.scenario.blue_tank_2.done = False
            blue_observation, blue_reward, blue_done = player_4.blue_choose_action(wargame_town)
            if RENDER:
                wargame_town.render()
            if wargame_town.check_win():
                second_episode_num += 1
                wargame_town.reset()
                print("Second Half %s :Red Win %s,Blue Win %s" % (
                    second_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                RV.data_update(wargame_town)
            else:
                wargame_town.scenario.red_tank_1.done = True
                wargame_town.scenario.red_tank_2.done = True
                wargame_town.scenario.blue_tank_1.done = False
                wargame_town.scenario.blue_tank_2.done = False
                if len(wargame_town.scenario.blue_tank_1.action_history) < wargame_town.rounds:
                    wargame_town.scenario.blue_tank_1.action_history.append('pass')
                    wargame_town.scenario.blue_tank_1.hex_history.append((0, 0))
                if len(wargame_town.scenario.blue_tank_2.action_history) < wargame_town.rounds:
                    wargame_town.scenario.blue_tank_2.action_history.append('pass')
                    wargame_town.scenario.blue_tank_2.hex_history.append((0, 0))
    print('Second Half End')
    second_record_score(wargame_town)
    wargame_town.hud.show_end_popup = True
    wargame_town.hud.show_end()
    wargame_town.destroy()
    RV.output()


if __name__ == '__main__':

    # wargame_town = Wargame_env()
    run_wargame(player_4, player_2)
