# -*- coding: utf-8 -*-
# @Time : 2021/5/12 19:37
# 环境相关函数接口说明
# ————————————————————————————————
#
# 本环境红蓝双方各有两个算子（类）
# 红方算子包括 wargame.scenario.red_tank_1, wargame.scenario.red_tank_2
# 蓝方算子包括 wargame.scenario.blue_tank_1, wargame.scenario.blue_tank_2

# 每个算子包含 4 个方法
# 机动，遮蔽，直瞄射击，间瞄射击
#
# 方法1  机动（仅可机动一格）
#
# move_one_step(x,y)
# 输入x,y为int，代表相邻六角格的坐标，输出效果，算子移动
#
# 样例 如让红方坦克1机动到1708六角格
# tank = wargame.scenario.red_tank_1
# tank.move_one_step(17,8)
# 当红方坦克1距离1708仅1格时，红方坦克机动到1708
#
# 方法2 遮蔽
#
# change_to_hide_state()
# 无需传入参数
#
# 样例 如让红方坦克1进入遮蔽状态
# tank = wargame.scenario.red_tank_1
# tank.change_to_hide_state()
# 红方坦克1进入遮蔽状态
#
# 方法3 直瞄射击
#
# direct_fire(enermy)
# 输入enermy为算子，输出效果，射击enermy
#
# 样例 如让红方坦克1直瞄射击蓝方坦克2
# tank = wargame.scenario.red_tank_1
# enermy = wargame.scenario.blue_tank_2
# tank.direct_fire(enermy)
# 红方坦克1直瞄射击蓝方坦克2
#
# 方法4 间瞄射击
#
# indirect_fire(x,y)
# 输入x，y为int，代表目标六角格坐标，输出效果，间瞄目标六角格
#
# 样例 如让红方坦克1间瞄射击六角格1624
# tank = wargame.scenario.red_tank_1
# tank.indirect_fire(16，24)
# 红方坦克1间瞄射击六角格1624

# 算子相关属性及函数
#
# 1 获得算子所处的六角格坐标
# piece.co_x,piece.co_y
#
# 样例 如要得到蓝方坦克1的六角格坐标位置
# tank = wargame.scenario.blue_tank_1
# x,y = tank.co_x,tank.co_y
# print(x,y)
# >> 15 40

# 2 检查算子是否能观察到对方算子
# piece.check_watch(enermy):
# 输入enermy为算子，代表敌方算子，返回True则可观察到，返回False则不可观察到
#
# 样例 检查红方坦克1是否能观察到蓝方坦克1
# tank = wargame.scenario.red_tank_1
# enermy = wargame.scenario.blue_tank_1
# watch = tank.check_watch(enermy)
# print(watch)
# >> False

# 3 获得算子对敌方算子的攻击等级
# self.check_rank(enermy):
# 输入enermy为算子，代表敌方算子，返回int 代表攻击等级
#
# 样例 获得红方坦克1对蓝方坦克2的攻击等级
# tank = wargame.scenario.red_tank_1
# enermy = wargame.scenario.blue_tank_2
# rank = tank.check_rank(enermy)
# print(rank)
# >> 2





# 地图查询接口
# 接口1 查询六角格周围的格子坐标
#
# wargame.game_map.get_neighbour(x,y)
# 输入x,y为int，代表六角格的坐标，输出 list，以列表形式表示周围六角格坐标
#
# 样例如查询1707周边的六角格坐标
# n = wargame.game_map.get_neighbour(17, 7)
# print(n)
# >> [(17, 6), (17, 8), (16, 7), (16, 8), (18, 7), (18, 8)]

# 接口2 查询两个六角格之间距离
# wargame.game_map.get_distance_between_hex(x0,y0,x1,y1)
# 输入x0,y0,x1,y1为int，表示起点六角格坐标和终点六角格坐标，输出int，表示两个六角格之间距离
#
# 样例如查询1707到1624之间的距离
# d = wargame.game_map.get_distance_between_hex(17, 7, 16, 24)
# print(d)
# >> 17

# 接口3 查询两个六角格是否通视
# wargame.game_map.visibility_estimation(x0,y0,x1,y1)
# 输入x0，y0，x1，y1为int，表示起点六角格坐标和终点六角格坐标，返回True可通视，返回False不可通视
#
# 样例如查询1707和1624是否通视
# visibility = wargame.game_map.visibility_estimation(17,7,16,24)
# print(visibility)
# >> False

import random
# import tensorflow
NAME = '战队1'




def red_choose_action(wargame):
    tank_1 = wargame.scenario.red_tank_1
    tank_2 = wargame.scenario.red_tank_2
    e_tank_1 = wargame.scenario.blue_tank_1
    e_tank_2 = wargame.scenario.blue_tank_2
    offline_potiential = wargame.game_map.offline_potiential
    neighbours1 = wargame.game_map.get_neighbour(tank_1.co_x,tank_1.co_y)


    goal_result = 0
    fire_result = 0
    # -------Tank1 AI-------
    e1 = {}
    d1 = {}
    current_offline_energy1 = offline_potiential.get((tank_1.co_x, tank_1.co_y), 0)
    max_energy1 = current_offline_energy1
    for neighbour in neighbours1:
        if neighbour not in tank_1.move_history:
            e1[neighbour] = offline_potiential.get(neighbour, 0)
            d1[neighbour] = tank_1.wargame_env.game_map.get_distance_between_hex(tank_1.goal[0], tank_1.goal[1],
                                                                              neighbour[0], neighbour[1])
            max_energy1 = e1[neighbour] if e1[neighbour] > current_offline_energy1 else current_offline_energy1
    e_neighbour1 = max(e1, key=e1.get)
    d_neighbour1 = min(d1, key=d1.get)
    # tank_1.move_one_step(d_neighbour1[0], d_neighbour1[1])
    tank_1.change_to_hide_state()
    result1 = 0
    # -------Tank2 AI-------
    tank_2 = wargame.scenario.red_tank_2
    neighbours2 = wargame.game_map.get_neighbour(tank_2.co_x,tank_2.co_y)
    e2 = {}
    d2 = {}
    current_offline_energy2 = offline_potiential.get((tank_2.co_x, tank_2.co_y), 0)
    max_energy2 = current_offline_energy2
    for neighbour in neighbours2:
        if neighbour not in tank_2.move_history:
            e2[neighbour] = offline_potiential.get(neighbour, 0)
            d2[neighbour] = tank_2.wargame_env.game_map.get_distance_between_hex(tank_2.goal[0], tank_2.goal[1],
                                                                              neighbour[0], neighbour[1])
            max_energy1 = e2[neighbour] if e2[neighbour] > current_offline_energy2 else current_offline_energy2
    e_neighbour2 = max(e2, key=e2.get)
    d_neighbour2 = min(d2, key=d2.get)
    tank_2.move_one_step(d_neighbour2[0], d_neighbour2[1])
    result2 = 0
    # if current_offline_energy == max_energy:
    #     n = random.random()
    #     if n < 0.5:
    #         action = tank_1.actions[7]
    #         fire_result = tank_1.direct_fire(e_tank_1)
    #     elif n < 0.7:
    #         action = tank_1.actions[8]
    #         tank_1.indirect_fire(e_tank_1)
    #     elif n < 0.9:
    #         action = tank_1.actions[6]
    #         tank_1.change_to_hide_state()
    #         goal_result = tank_1.get_punishment()
    #     else:
    #         tank_1.move_one_step(d_neighbour[0], d_neighbour[1])
    #         print('R1 Move_to:', d_neighbour[0], d_neighbour[1])
    #         goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
    # else:
    #     n = random.random()
    #     if n < 0.5:
    #         tank_1.move_one_step(d_neighbour[0], d_neighbour[1])
    #         goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
    #     elif n < 0.8:
    #         tank_1.move_one_step(e_neighbour[0], e_neighbour[1])
    #         goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
    #     if n < 1:
    #         tank_1.change_to_fire_state()
    #         action = tank_1.actions[7]
    #         fire_result = tank_1.direct_fire(e_tank_1)
    #     elif n < 0.9:
    #         action = tank_1.actions[8]
    #         tank_1.indirect_fire(e_tank_1)
    #     else:
    #         action = tank_1.actions[6]
    #         tank_1.change_to_hide_state()
    #         goal_result = tank_1.get_punishment()
    #
    # result = goal_result + fire_result

    # # return [tank_1.state_history[-1],tank_1.get_piece_state(),tank_1.action_history[-1],tank_1.hex_history[-1],
    #         tank_2.state_history[-1], tank_2.get_piece_state(),tank_2.action_history[-1],tank_2.hex_history[-1]
    #         ]
    return

def blue_choose_action(wargame):
    tank_1 = wargame.scenario.blue_tank_1
    e_tank_1 = wargame.scenario.red_tank_1
    offline_potiential = wargame.game_map.offline_potiential
    neighbours = wargame.game_map.get_neighbour(tank_1.co_x, tank_1.co_y)

    goal_result = 0
    fire_result = 0

    e = {}
    d = {}
    current_offline_energy = offline_potiential.get((tank_1.co_x, tank_1.co_y), 0)
    max_energy = current_offline_energy
    for neighbour in neighbours:
        if neighbour not in tank_1.move_history:
            e[neighbour] = offline_potiential.get(neighbour, 0)
            d[neighbour] = tank_1.wargame_env.game_map.get_distance_between_hex(tank_1.goal[0], tank_1.goal[1],
                                                                              neighbour[0], neighbour[1])
            max_energy = e[neighbour] if e[neighbour] > current_offline_energy else current_offline_energy
    e_neighbour = max(e, key=e.get)
    d_neighbour = min(d, key=d.get)
    # if current_offline_energy == max_energy:
    #     n = random.random()
    #     if n < 0.5:
    #         tank_1.change_to_fire_state()
    #         action = tank_1.actions[7]
    #         fire_result = tank_1.direct_fire(e_tank_1)
    #     elif n < 0.7:
    #         action = tank_1.actions[8]
    #         tank_1.indirect_fire(18,8)
    #     elif n < 0.9:
    #         action = tank_1.actions[6]
    #         tank_1.change_to_hide_state()
    #         goal_result = tank_1.get_punishment()
    #     else:
    #         tank_1.change_to_move_state()
    #         tank_1.move_one_step(d_neighbour[0], d_neighbour[1])
    #         goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
    # else:
    n = random.random()
    if n < 0.4:
        tank_1.change_to_move_state()
        tank_1.move_one_step(d_neighbour[0], d_neighbour[1])
        goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
    elif n < 0.5:
        tank_1.change_to_move_state()
        tank_1.move_one_step(e_neighbour[0], e_neighbour[1])
        goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
    if n < 0.7:
        tank_1.change_to_fire_state()
        action = tank_1.actions[7]
        fire_result = tank_1.direct_fire(e_tank_1)
    elif n < 0.9:
        action = tank_1.actions[8]
        tank_1.indirect_fire(18,8)
    else:
        action = tank_1.actions[6]
        tank_1.change_to_hide_state()
        goal_result = tank_1.get_punishment()



    return tank_1.get_piece_state(), 0, tank_1.done

