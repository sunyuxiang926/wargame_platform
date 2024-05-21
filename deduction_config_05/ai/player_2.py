import random
import pandas as pd
from deduction_config_05.ai.util import *
from deduction_config_05.ai.masac import *
from operational_assessment_06.MySql import Mysql
from platform_settings_07.wargame_env import Wargame_env
from importlib import import_module
from ResultVisualization import ResultVisualization

NAME = '战队2'


def red_choose_action(wargame):
    tank_1 = wargame.scenario.red_tank_1
    offline_potiential = wargame.game_map.offline_potiential
    neighbours = wargame.game_map.get_neighbour(tank_1.co_x,tank_1.co_y)
    e_tank_1 = wargame.scenario.blue_tank_1
    e_tank_2 = wargame.scenario.blue_tank_2

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
    if current_offline_energy == max_energy:
        n = random.random()
        if n < 0.5:
            tank_1.change_to_fire_state()
            action = tank_1.actions[7]
            fire_result = tank_1.direct_fire(e_tank_1)
        elif n < 0.9:
            action = tank_1.actions[8]
            tank_1.indirect_fire(16, 41)
        elif n < 0.9:
            action = tank_1.actions[6]
            tank_1.change_to_hide_state()
            goal_result = tank_1.get_punishment()
        else:
            tank_1.change_to_move_state()
            tank_1.move_one_step(d_neighbour[0], d_neighbour[1])
            goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
    else:
        n = random.random()
        if n < 1:
            tank_1.change_to_move_state()
            tank_1.move_one_step(d_neighbour[0], d_neighbour[1])
            goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
        elif n < 0.8:
            tank_1.change_to_move_state()
            tank_1.move_one_step(e_neighbour[0], e_neighbour[1])
            goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
        if n < 0.7:
            tank_1.change_to_fire_state()
            action = tank_1.actions[7]
            fire_result = tank_1.direct_fire(e_tank_1)
        elif n < 0.9:
            action = tank_1.actions[8]
            tank_1.indirect_fire(16, 41)
        else:
            action = tank_1.actions[6]
            tank_1.change_to_hide_state()
            goal_result = tank_1.get_punishment()
    return tank_1.get_piece_state(), 0, tank_1.done


def blue_choose_action(wargame):

    # UAV_list = [1, 1, 1, 1]
    UAV_list = [1, 1, 1, 1]

    tank_1 = wargame.scenario.blue_tank_1
    tank_2 = wargame.scenario.blue_tank_2
    tank_3 = wargame.scenario.blue_tank_3
    tank_4 = wargame.scenario.blue_tank_4
    tank_5 = wargame.scenario.blue_tank_5
    tank_6 = wargame.scenario.blue_tank_6
    tank_7 = wargame.scenario.blue_tank_7
    tank_8 = wargame.scenario.blue_tank_8
    tank_9 = wargame.scenario.blue_tank_9
    tank_10 = wargame.scenario.blue_tank_10

    r_tank_1 = wargame.scenario.red_tank_1
    r_tank_2 = wargame.scenario.red_tank_2
    r_tank_3 = wargame.scenario.red_tank_3
    r_tank_4 = wargame.scenario.red_tank_4
    r_tank_5 = wargame.scenario.red_tank_5
    r_tank_6 = wargame.scenario.red_tank_6
    r_tank_7 = wargame.scenario.red_tank_7
    r_tank_8 = wargame.scenario.red_tank_8

    if UAV_list[0] == 1:
        r_plane_9 = wargame.scenario.red_plane_9
    else:
        pass

    if UAV_list[1] == 1:
        r_plane_10 = wargame.scenario.red_plane_10
    else:
        pass

    if UAV_list[2] == 1:
        r_plane_11 = wargame.scenario.red_plane_11
    else:
        pass

    if UAV_list[3] == 1:
        r_plane_12 = wargame.scenario.red_plane_12
    else:
        pass

    offline_potiential = wargame.game_map.offline_potiential
    neighbours1 = wargame.game_map.get_neighbour(tank_1.co_x, tank_1.co_y)
    neighbours2 = wargame.game_map.get_neighbour(tank_2.co_x, tank_2.co_y)
    neighbours3 = wargame.game_map.get_neighbour(tank_3.co_x, tank_3.co_y)
    neighbours4 = wargame.game_map.get_neighbour(tank_4.co_x, tank_4.co_y)
    neighbours5 = wargame.game_map.get_neighbour(tank_5.co_x, tank_5.co_y)
    neighbours6 = wargame.game_map.get_neighbour(tank_6.co_x, tank_6.co_y)
    neighbours7 = wargame.game_map.get_neighbour(tank_7.co_x, tank_7.co_y)
    neighbours8 = wargame.game_map.get_neighbour(tank_8.co_x, tank_8.co_y)
    neighbours9 = wargame.game_map.get_neighbour(tank_9.co_x, tank_9.co_y)
    neighbours10 = wargame.game_map.get_neighbour(tank_10.co_x, tank_10.co_y)
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
    result1 = 0
    # -------Tank2 AI-------
    e2 = {}
    d2 = {}
    current_offline_energy2 = offline_potiential.get((tank_2.co_x, tank_2.co_y), 0)
    max_energy2 = current_offline_energy2
    for neighbour in neighbours2:
        if neighbour not in tank_2.move_history:
            e2[neighbour] = offline_potiential.get(neighbour, 0)
            d2[neighbour] = tank_2.wargame_env.game_map.get_distance_between_hex(tank_2.goal[0], tank_2.goal[1],
                                                                                 neighbour[0], neighbour[1])
            max_energy2 = e2[neighbour] if e2[neighbour] > current_offline_energy2 else current_offline_energy2
    e_neighbour2 = max(e2, key=e2.get)
    d_neighbour2 = min(d2, key=d2.get)
    # tank_2.move_one_step(d_neighbour2[0], d_neighbour2[1])
    result2 = 0
    # -----------Tank3 AI-----------
    e3 = {}
    d3 = {}
    current_offline_energy3 = offline_potiential.get((tank_3.co_x, tank_3.co_y), 0)
    max_energy3 = current_offline_energy3
    for neighbour in neighbours3:
        if neighbour not in tank_3.move_history:
            e3[neighbour] = offline_potiential.get(neighbour, 0)
            d3[neighbour] = tank_3.wargame_env.game_map.get_distance_between_hex(tank_3.goal[0], tank_3.goal[1],
                                                                                 neighbour[0], neighbour[1])
            max_energy3 = e3[neighbour] if e3[neighbour] > current_offline_energy3 else current_offline_energy3
    e_neighbour3 = max(e3, key=e3.get)
    d_neighbour3 = min(d3, key=d3.get)
    result3 = 0
    # # -----------Tank4 AI-----------
    e4 = {}
    d4 = {}
    current_offline_energy4 = offline_potiential.get((tank_4.co_x, tank_4.co_y), 0)
    max_energy4 = current_offline_energy4
    for neighbour in neighbours4:
        if neighbour not in tank_4.move_history:
            e4[neighbour] = offline_potiential.get(neighbour, 0)
            d4[neighbour] = tank_4.wargame_env.game_map.get_distance_between_hex(tank_4.goal[0], tank_4.goal[1],
                                                                                 neighbour[0], neighbour[1])
            max_energy4 = e4[neighbour] if e4[neighbour] > current_offline_energy4 else current_offline_energy4
    e_neighbour4 = max(e4, key=e4.get)
    d_neighbour4 = min(d4, key=d4.get)
    result4 = 0
    # -------Tank5 AI-------
    e5 = {}
    d5 = {}
    current_offline_energy5= offline_potiential.get((tank_5.co_x, tank_5.co_y), 0)
    max_energy5 = current_offline_energy5
    for neighbour in neighbours5:
        if neighbour not in tank_5.move_history:
            e5[neighbour] = offline_potiential.get(neighbour, 0)
            d5[neighbour] = tank_5.wargame_env.game_map.get_distance_between_hex(tank_5.goal[0], tank_5.goal[1],
                                                                                 neighbour[0], neighbour[1])
            max_energy5 = e5[neighbour] if e5[neighbour] > current_offline_energy5 else current_offline_energy5
    e_neighbour5 = max(e5, key=e5.get)
    d_neighbour5 = min(d5, key=d5.get)
    # tank_1.move_one_step(d_neighbour1[0], d_neighbour1[1])
    result5 = 0
    # -------Tank6 AI-------
    e6 = {}
    d6 = {}
    current_offline_energy6 = offline_potiential.get((tank_6.co_x, tank_6.co_y), 0)
    max_energy6 = current_offline_energy6
    for neighbour in neighbours6:
        if neighbour not in tank_6.move_history:
            e6[neighbour] = offline_potiential.get(neighbour, 0)
            d6[neighbour] = tank_6.wargame_env.game_map.get_distance_between_hex(tank_6.goal[0], tank_6.goal[1],
                                                                                 neighbour[0], neighbour[1])
            max_energy6 = e6[neighbour] if e6[neighbour] > current_offline_energy6 else current_offline_energy6
    e_neighbour6 = max(e6, key=e6.get)
    d_neighbour6 = min(d6, key=d6.get)
    # tank_6.move_one_step(d_neighbour6[0], d_neighbour6[1])
    result6 = 0
    # -------Tank7 AI-------
    e7 = {}
    d7 = {}
    current_offline_energy7 = offline_potiential.get((tank_7.co_x, tank_7.co_y), 0)
    max_energy7 = current_offline_energy7
    for neighbour in neighbours7:
        if neighbour not in tank_7.move_history:
            e7[neighbour] = offline_potiential.get(neighbour, 0)
            d7[neighbour] = tank_7.wargame_env.game_map.get_distance_between_hex(tank_7.goal[0], tank_7.goal[1],
                                                                                 neighbour[0], neighbour[1])
            max_energy7 = e7[neighbour] if e7[neighbour] > current_offline_energy7 else current_offline_energy7
    e_neighbour7 = max(e7, key=e7.get)
    d_neighbour7 = min(d7, key=d7.get)
    # tank_7.move_one_step(d_neighbour7[0], d_neighbour7[1])
    result7 = 0
    # -------Tank8 AI-------
    e8 = {}
    d8 = {}
    current_offline_energy8 = offline_potiential.get((tank_8.co_x, tank_8.co_y), 0)
    max_energy8 = current_offline_energy8
    for neighbour in neighbours8:
        if neighbour not in tank_8.move_history:
            e8[neighbour] = offline_potiential.get(neighbour, 0)
            d8[neighbour] = tank_8.wargame_env.game_map.get_distance_between_hex(tank_8.goal[0], tank_8.goal[1],
                                                                                 neighbour[0], neighbour[1])
            max_energy8 = e8[neighbour] if e8[neighbour] > current_offline_energy8 else current_offline_energy8
    e_neighbour8 = max(e8, key=e8.get)
    d_neighbour8 = min(d8, key=d8.get)
    # tank_8.move_one_step(d_neighbour8[0], d_neighbour8[1])
    result8 = 0
    
    # -------Tank9 AI-------
    e9 = {}
    d9 = {}
    current_offline_energy9 = offline_potiential.get((tank_9.co_x, tank_9.co_y), 0)
    max_energy9 = current_offline_energy9
    for neighbour in neighbours9:
        if neighbour not in tank_9.move_history:
            e9[neighbour] = offline_potiential.get(neighbour, 0)
            d9[neighbour] = tank_9.wargame_env.game_map.get_distance_between_hex(tank_9.goal[0], tank_9.goal[1],
                                                                                 neighbour[0], neighbour[1])
            max_energy9 = e9[neighbour] if e9[neighbour] > current_offline_energy9 else current_offline_energy9
    e_neighbour9 = max(e9, key=e9.get)
    d_neighbour9 = min(d9, key=d9.get)
    # tank_9.move_one_step(d_neighbour9[0], d_neighbour9[9])
    result9 = 0
    # -------Tank10 AI-------
    e10 = {}
    d10 = {}
    current_offline_energy10 = offline_potiential.get((tank_10.co_x, tank_10.co_y), 0)
    max_energy10 = current_offline_energy10
    for neighbour in neighbours10:
        if neighbour not in tank_10.move_history:
            e10[neighbour] = offline_potiential.get(neighbour, 0)
            d10[neighbour] = tank_10.wargame_env.game_map.get_distance_between_hex(tank_10.goal[0], tank_10.goal[1],
                                                                                 neighbour[0], neighbour[1])
            max_energy10 = e10[neighbour] if e10[neighbour] > current_offline_energy10 else current_offline_energy10
    e_neighbour10 = max(e10, key=e10.get)
    d_neighbour10 = min(d10, key=d10.get)
    # tank_10.move_one_step(d_neighbour10[0], d_neighbour10[10])
    result10 = 0
    # if current_offline_energy1 == max_energy1:

    if tank_1.num>0:
        n = random.random()
        # print('B1 n=', n)
        if n < 0.1:
            action = tank_1.actions[7]
            tank_1.change_to_fire_state()
            fire_result = tank_1.direct_fire(r_tank_1)
        elif n < 0.2:
            action = tank_1.actions[8]
            tank_1.indirect_fire(17, 7)
        elif n < 0.6:
            action = tank_1.actions[6]
            tank_1.change_to_hide_state()
            goal_result = tank_1.get_punishment()
        else:
            tank_1.move_one_step(d_neighbour1[0], d_neighbour1[1])
            # print('B1 dMove_to:', d_neighbour1[0], d_neighbour1[1])
            goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
    # else:
    #     n = random.random()
    #     if n < 0.2:
    #         tank_1.move_one_step(d_neighbour1[0], d_neighbour1[1])
    #         print('B11 dMove_to:', e_neighbour1[0], e_neighbour1[1])
    #         goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
    #     elif n < 0.4:
    #         tank_1.move_one_step(e_neighbour1[0], e_neighbour1[1])
    #         print('B11 eMove_to:', e_neighbour1[0], e_neighbour1[1])
    #         goal_result = tank_1.get_goal_reward() + tank_1.get_punishment()
    #     elif n < 0.7:
    #         tank_1.change_to_fire_state()
    #         action = tank_1.actions[7]
    #         fire_result = tank_1.direct_fire(e_tank_1)
    #     elif n < 1:
    #         action = tank_1.actions[8]
    #         tank_1.indirect_fire(17,7)
    #     else:
    #         action = tank_1.actions[6]
    #         tank_1.change_to_hide_state()
    #         goal_result = tank_1.get_punishment()
    # #
    # result = goal_result + fire_result
    # if current_offline_energy2 == max_energy2:
    if tank_2.num>0:
        n = random.random()
        # print('B2 n=', n)
        if n < 0.1:
            action = tank_2.actions[7]
            tank_2.change_to_fire_state()
            fire_result = tank_2.direct_fire(r_tank_2)
        elif n < 0.2:
            action = tank_2.actions[8]
            tank_2.indirect_fire(17, 7)
        elif n < 0.7:
            action = tank_2.actions[6]
            tank_2.change_to_hide_state()
            goal_result = tank_2.get_punishment()
        else:
            tank_2.move_one_step(d_neighbour2[0], d_neighbour2[1])
            # print('B2 dMove_to:', d_neighbour2[0], d_neighbour2[1])
            goal_result = tank_2.get_goal_reward() + tank_2.get_punishment()
    # else:
    #     n = random.random()
    #     if n < 0.4:
    #         tank_2.move_one_step(d_neighbour2[0], d_neighbour2[1])
    #         print('B22 dMove_to:', d_neighbour2[0], d_neighbour2[1])
    #         goal_result = tank_2.get_goal_reward() + tank_2.get_punishment()
    #     elif n < 0.6:
    #         tank_2.move_one_step(e_neighbour2[0], e_neighbour2[1])
    #         print('B22 eMove_to:', e_neighbour2[0], e_neighbour2[1])
    #         goal_result = tank_2.get_goal_reward() + tank_2.get_punishment()
    #     elif n < 0.8:
    #         tank_2.change_to_fire_state()
    #         action = tank_2.actions[7]
    #         fire_result = tank_2.direct_fire(e_tank_2)
    #     elif n < 0.9:
    #         action = tank_2.actions[8]
    #         tank_2.indirect_fire(17,7)
    #     else:
    #         action = tank_2.actions[6]
    #         tank_2.change_to_hide_state()
    #         goal_result = tank_2.get_punishment()
    # #
    # # result = goal_result + fire_result
    # return tank_1.get_piece_state(), result1, tank_1.done, tank_2.get_piece_state(), result2, tank_2.done
    if tank_3.num>0:
        n = random.random()
        # print('B3 n=', n)
        if n < 0.1:
            action = tank_3.actions[7]
            tank_3.change_to_fire_state()
            fire_result = tank_3.direct_fire(r_tank_3)
        elif n < 0.2:
            action = tank_3.actions[8]
            tank_3.indirect_fire(17, 7)
        elif n < 0.7:
            action = tank_3.actions[6]
            tank_3.change_to_hide_state()
            goal_result = tank_3.get_punishment()
        else:
            tank_3.move_one_step(d_neighbour3[0], d_neighbour3[1])
            # print('B3 dMove_to:', d_neighbour3[0], d_neighbour3[1])
            goal_result = tank_3.get_goal_reward() + tank_3.get_punishment()

    if tank_4.num>0:
        n = random.random()
        # print('B4 n=', n)
        if n < 0.1:
            action = tank_4.actions[7]
            tank_4.change_to_fire_state()
            fire_result = tank_4.direct_fire(r_tank_4)
        elif n < 0.2:
            action = tank_4.actions[8]
            tank_4.indirect_fire(17, 7)
        elif n < 0.7:
            action = tank_4.actions[6]
            tank_4.change_to_hide_state()
            goal_result = tank_4.get_punishment()
        else:
            tank_4.move_one_step(d_neighbour4[0], d_neighbour4[1])
            # print('B4 dMove_to:', d_neighbour4[0], d_neighbour4[1])
            goal_result = tank_4.get_goal_reward() + tank_4.get_punishment()

    if tank_5.num>0:
        n = random.random()
        # print('B5 n=', n)
        if n < 0.1:
            action = tank_5.actions[7]
            tank_5.change_to_fire_state()
            fire_result = tank_5.direct_fire(r_tank_5)
        elif n < 0.2:
            action = tank_5.actions[8]
            tank_5.indirect_fire(17, 7)
        elif n < 0.7:
            action = tank_5.actions[6]
            tank_5.change_to_hide_state()
            goal_result = tank_5.get_punishment()
        else:
            tank_5.move_one_step(d_neighbour5[0], d_neighbour5[1])
            # print('B5 dMove_to:', d_neighbour5[0], d_neighbour5[1])
            goal_result = tank_5.get_goal_reward() + tank_5.get_punishment()

    if tank_6.num>0:
        n = random.random()
        # print('B6 n=', n)
        if n < 0.1:
            action = tank_6.actions[7]
            tank_6.change_to_fire_state()
            fire_result = tank_6.direct_fire(r_tank_6)
        elif n < 0.2:
            action = tank_6.actions[8]
            tank_6.indirect_fire(17, 7)
        elif n < 0.7:
            action = tank_6.actions[6]
            tank_6.change_to_hide_state()
            goal_result = tank_6.get_punishment()
        else:
            tank_6.move_one_step(d_neighbour6[0], d_neighbour6[1])
            # print('B6 dMove_to:', d_neighbour6[0], d_neighbour6[1])
            goal_result = tank_6.get_goal_reward() + tank_6.get_punishment()

    if tank_7.num>0:
        n = random.random()
        # print('B7 n=', n)
        if n < 0.1:
            action = tank_7.actions[7]
            tank_7.change_to_fire_state()
            fire_result = tank_7.direct_fire(r_tank_7)
        elif n < 0.2:
            action = tank_7.actions[8]
            tank_7.indirect_fire(17, 7)
        elif n < 0.8:
            action = tank_7.actions[6]
            tank_7.change_to_hide_state()
            goal_result = tank_7.get_punishment()
        else:
            tank_7.move_one_step(d_neighbour7[0], d_neighbour7[1])
            # print('B7 dMove_to:', d_neighbour7[0], d_neighbour7[1])
            goal_result = tank_7.get_goal_reward() + tank_7.get_punishment()

    if tank_8.num>0:
        n = random.random()
        # print('B8 n=', n)
        if n < 0.1:
            action = tank_8.actions[7]
            tank_8.change_to_fire_state()
            if UAV_list[0] == 1:
                fire_result = tank_8.direct_fire(r_tank_8)
        elif n < 0.2:
            action = tank_8.actions[8]
            tank_8.indirect_fire(17, 7)
        elif n < 0.7:
            action = tank_8.actions[6]
            tank_8.change_to_hide_state()
            goal_result = tank_8.get_punishment()
        else:
            tank_8.move_one_step(d_neighbour8[0], d_neighbour8[1])
            # print('B8 dMove_to:', d_neighbour8[0], d_neighbour8[1])
            goal_result = tank_8.get_goal_reward() + tank_8.get_punishment()

    if tank_9.num>0:
        n = random.random()
        # print('B9 n=', n)
        if n < 0.1:
            action = tank_9.actions[7]
            tank_9.change_to_fire_state()
            if UAV_list[1] == 1:
                fire_result = tank_9.direct_fire(r_tank_8)
        elif n < 0.2:
            action = tank_9.actions[8]
            tank_9.indirect_fire(17, 7)
        elif n < 0.7:
            action = tank_9.actions[6]
            tank_9.change_to_hide_state()
            goal_result = tank_9.get_punishment()
        else:
            tank_9.move_one_step(d_neighbour9[0], d_neighbour9[1])
            # print('B9 dMove_to:', d_neighbour9[0], d_neighbour9[1])
            goal_result = tank_9.get_goal_reward() + tank_9.get_punishment()

    if tank_10.num>0:
        n = random.random()
        # print('B10 n=', n)
        if n < 0.1:
            action = tank_10.actions[7]
            tank_10.change_to_fire_state()
            if UAV_list[2] == 1:
                fire_result = tank_10.direct_fire(r_tank_7)
        elif n < 0.2:
            action = tank_10.actions[8]
            tank_10.indirect_fire(17, 7)
        elif n < 0.7:
            action = tank_10.actions[6]
            tank_10.change_to_hide_state()
            goal_result = tank_10.get_punishment()
        else:
            tank_10.move_one_step(d_neighbour10[0], d_neighbour10[1])
            # print('B10 dMove_to:', d_neighbour10[0], d_neighbour10[1])
            goal_result = tank_10.get_goal_reward() + tank_10.get_punishment()

    return
