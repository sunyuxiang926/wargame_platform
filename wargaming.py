# import类似DOS命令操作：如果指向文件夹，则导入其中的py文件；
# 如果指向文件夹中的py文件，则导入其中的类或函数。
# 本文件是兵棋大环境，包括地图，算子，交互控制等全部对象。

# from deduction_config_05.ai.RL_brain import DeepQNetwork
from deduction_config_05.ai import player_1, player_2
import sys
from operational_assessment_06.MySql import Mysql
from platform_settings_07.wargame_env import Wargame_env
import numpy as np
import pandas as pd

mywargame_sql = Mysql("mysql")
from importlib import import_module
from ResultVisualization import ResultVisualization

from pieces_manager_02.piece import RTank
from pieces_manager_02.piece import BTank

red_done = False
blue_done = False

def get_position(piece):
    position_xyz = piece.get_xyz()
    position_ID = position_xyz[0] * 100 + position_xyz[1]
    return position_ID


def get_distance_between_hex(hex_1_x, hex_1_y, hex_2_x, hex_2_y):
    def oddr_to_cube(row, col):
        x = col - (row - (row & 1)) / 2
        z = row
        y = -x - z
        return (x, y, z)

    start = oddr_to_cube(hex_1_x, hex_1_y)
    end = oddr_to_cube(hex_2_x, hex_2_y)
    return int(max(abs(start[0] - end[0]), abs(start[1] - end[1]), abs(start[2] - end[2])))


def first_record_score(wargame_town):
    # player1的统计数据
    wargame_town.p1_red_kill_score = wargame_town.red_kill_score
    wargame_town.p1_red_get_goal_score = wargame_town.red_get_goal_score
    wargame_town.p1_red_survive_score = wargame_town.red_survive_score
    wargame_town.p1_red_win_times = wargame_town.red_win_times
    # player2的统计数据
    wargame_town.p2_blue_kill_score = wargame_town.blue_kill_score
    wargame_town.p2_blue_get_goal_score = wargame_town.blue_get_goal_score
    wargame_town.p2_blue_survive_score = wargame_town.blue_survive_score
    wargame_town.p2_blue_win_times = wargame_town.blue_win_times

    # 双方数据初始化
    wargame_town.red_kill_score = 0
    wargame_town.red_get_goal_score = 0
    wargame_town.red_survive_score = 0

    wargame_town.blue_kill_score = 0
    wargame_town.blue_get_goal_score = 0
    wargame_town.blue_survive_score = 0
    wargame_town.red_win_times = 0
    wargame_town.blue_win_times = 0


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


def run_wargame(p1, p2):
    # a = p1.rsplit('/', 1)
    # print(a)
    # path = a[0]
    # print(path)
    # f = a[1].rsplit('.', 1)
    # print(f)
    # sys.path.append(path)
    # player_1 = import_module(f[0])

    # a = p2.rsplit('/', 1)
    # path = a[0]
    # f = a[1].rsplit('.', 1)
    # sys.path.append(path)
    # player_2 = import_module(f[0])

    wargame_town = Wargame_env()
    wargame_town.p1_name = player_1.NAME
    wargame_town.p2_name = player_2.NAME

    # 上下半场的总局数
    first_half_episodes = 5
    second_half_episodes = 5

    # 上下半场的统计局数
    first_episode_num = 1
    second_episode_num = 1

    # 初始化ResultVisualization
    RV = ResultVisualization(first_half_episodes, second_half_episodes)

    # 初始化算子信息列表
    episode_num = []
    steps = []
    R1_gaochenglist, R1_statelist, R1_positionlist = [], [], []
    R2_gaochenglist, R2_statelist, R2_positionlist = [], [], []
    B1_gaochenglist, B1_statelist, B1_positionlist = [], [], []
    B2_gaochenglist, B2_statelist, B2_positionlist = [], [], []
    R1_to_obj_distancelist, R2_to_obj_distancelist, B1_to_obj_distancelist, B2_to_obj_distancelist = [], [], [], []
    R1B1_distancelist, R1B2_distancelist = [], []
    R2B1_distancelist, R2B2_distancelist = [], []



    while first_episode_num <= first_half_episodes:

        # 渲染兵棋对抗环境
        wargame_town.render()

        # 每个episode中的回合计数
        wargame_town.steps += 1
        print('------------------------------------------')

        # <editor-fold desc="读取当前回合行动之前的状态">
        wargame_town.scenario.red_tank_1.state_history.append(wargame_town.scenario.red_tank_1.get_piece_state())
        wargame_town.scenario.red_tank_2.state_history.append(wargame_town.scenario.red_tank_2.get_piece_state())
        wargame_town.scenario.blue_tank_1.state_history.append(wargame_town.scenario.blue_tank_1.get_piece_state())
        wargame_town.scenario.blue_tank_2.state_history.append(wargame_town.scenario.blue_tank_2.get_piece_state())

        R1_Move_History = ','.join([str(x) for x in wargame_town.scenario.red_tank_1.move_history])
        R2_Move_History = ','.join([str(x) for x in wargame_town.scenario.red_tank_2.move_history])
        B1_Move_History = ','.join([str(x) for x in wargame_town.scenario.blue_tank_1.move_history])
        B2_Move_History = ','.join([str(x) for x in wargame_town.scenario.blue_tank_2.move_history])
        # 记录红蓝双方每一局的对抗轨迹数据
        mywargame_sql.insert(
            "insert into move_history values(%s,%s,%s,%s,%s,%s)",
            [first_episode_num, wargame_town.steps, R1_Move_History, R2_Move_History, B1_Move_History,
             B2_Move_History])
        # </editor-fold>

        # 获取并添加算子相关数据到列表
        episode_num.append(first_episode_num)
        steps.append(wargame_town.steps)

        R1_gaocheng = wargame_town.scenario.red_tank_1.get_xyz()
        R1_height = R1_gaocheng[2]
        R1_position = (R1_gaocheng[0], R1_gaocheng[1])
        R1_gaochenglist.append(R1_height)
        R1_positionlist.append(R1_position)
        R1_state = wargame_town.scenario.red_tank_1.get_piece_state()
        R1_statelist.append(R1_state[1])

        R2_gaocheng = wargame_town.scenario.red_tank_2.get_xyz()
        R2_height = R2_gaocheng[2]
        R2_position = (R2_gaocheng[0], R2_gaocheng[1])
        R2_gaochenglist.append(R2_height)
        R2_positionlist.append(R2_position)
        R2_state = wargame_town.scenario.red_tank_2.get_piece_state()
        R2_statelist.append(R2_state[1])
        # 获取蓝1坦克高程、状态、位置
        B1_gaocheng = wargame_town.scenario.blue_tank_1.get_xyz()
        B1_height = B1_gaocheng[2]
        B1_position = (B1_gaocheng[0], B1_gaocheng[1])
        B1_gaochenglist.append(B1_height)
        B1_positionlist.append(B1_position)
        B1_state = wargame_town.scenario.blue_tank_1.get_piece_state()
        B1_statelist.append(B1_state[1])

        # 获取蓝2坦克高程、状态、位置
        B2_gaocheng = wargame_town.scenario.blue_tank_2.get_xyz()
        B2_height = B2_gaocheng[2]
        B2_position = (B2_gaocheng[0], B2_gaocheng[1])
        B2_gaochenglist.append(B2_height)
        B2_positionlist.append(B2_position)
        B2_state = wargame_town.scenario.blue_tank_2.get_piece_state()
        B2_statelist.append(B2_state[1])

        # 红蓝双方坦克算子距目标点距离，红方计算到坐标(13, 23)距离，蓝方计算到坐标(13, 24)距离
        R1_to_obj_distance = get_distance_between_hex(R1_gaocheng[0], R1_gaocheng[1], 13, 23)
        R1_to_obj_distancelist.append(R1_to_obj_distance)
        R2_to_obj_distance = get_distance_between_hex(R2_gaocheng[0], R2_gaocheng[1], 13, 23)
        R2_to_obj_distancelist.append(R2_to_obj_distance)
        B1_to_obj_distance = get_distance_between_hex(B1_gaocheng[0], B1_gaocheng[1], 13, 24)
        B1_to_obj_distancelist.append(B1_to_obj_distance)
        B2_to_obj_distance = get_distance_between_hex(B2_gaocheng[0], B2_gaocheng[1], 13, 24)
        B2_to_obj_distancelist.append(B2_to_obj_distance)
        # 红蓝算子坦克间距离
        R1B1_distance = get_distance_between_hex(R1_gaocheng[0], R1_gaocheng[1], B1_gaocheng[0], B1_gaocheng[1])
        R1B2_distance = get_distance_between_hex(R1_gaocheng[0], R1_gaocheng[1], B2_gaocheng[0], B2_gaocheng[1])
        R2B1_distance = get_distance_between_hex(R2_gaocheng[0], R2_gaocheng[1], B1_gaocheng[0], B2_gaocheng[1])
        R2B2_distance = get_distance_between_hex(R2_gaocheng[0], R2_gaocheng[1], B2_gaocheng[0], B2_gaocheng[1])
        R1B1_distancelist.append(R1B1_distance)
        R1B2_distancelist.append(R1B2_distance)
        R2B1_distancelist.append(R2B1_distance)
        R2B2_distancelist.append(R2B2_distance)

        wargame_town.check_indirect_fire('red')
        # 打开红方行动开关，关闭蓝方行动开关
        wargame_town.scenario.red_tank_1.done = False
        wargame_town.scenario.red_tank_2.done = False
        wargame_town.scenario.blue_tank_1.done = True
        wargame_town.scenario.blue_tank_2.done = True

        player_1.red_choose_action(wargame_town)
        # 判断是否取胜,重置
        if wargame_town.check_win():
            first_episode_num += 1
            print("上半场： 第%s episode 第%s step" % (first_episode_num, wargame_town.steps))
            wargame_town.reset()
            print("First Half %s :Red Win %s,Blue Win %s" % (
                first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
            RV.data_update(wargame_town)
        else:
            if len(wargame_town.scenario.red_tank_1.action_history) < wargame_town.steps:
                wargame_town.scenario.red_tank_1.action_history.append('pass')
                wargame_town.scenario.red_tank_1.hex_history.append((0, 0))
            if len(wargame_town.scenario.red_tank_2.action_history) < wargame_town.steps:
                wargame_town.scenario.red_tank_2.action_history.append('pass')
                wargame_town.scenario.red_tank_2.hex_history.append((0, 0))

            wargame_town.check_indirect_fire('blue')
            # 打开蓝方行动开关，关闭红方行动开关
            wargame_town.scenario.red_tank_1.done = True
            wargame_town.scenario.red_tank_2.done = True
            wargame_town.scenario.blue_tank_1.done = False
            wargame_town.scenario.blue_tank_2.done = False
            player_2.blue_choose_action(wargame_town)

            # # 判断是否取胜,重置
            if wargame_town.check_win():
                first_episode_num += 1
                wargame_town.reset()
                print("First Half %s :Red Win %s,Blue Win %s" % (
                    first_episode_num, wargame_town.red_win_times, wargame_town.blue_win_times))
                RV.data_update(wargame_town)
            else:
                if len(wargame_town.scenario.blue_tank_1.action_history) < wargame_town.steps:
                    wargame_town.scenario.blue_tank_1.action_history.append('pass')
                    wargame_town.scenario.blue_tank_1.hex_history.append((0, 0))
                if len(wargame_town.scenario.blue_tank_2.action_history) < wargame_town.steps:
                    wargame_town.scenario.blue_tank_2.action_history.append('pass')
                    wargame_town.scenario.blue_tank_2.hex_history.append((0, 0))

        # df_blue_state = pd.DataFrame(wargame_town.scenario.blue_tank_1.state_history,
        #                              wargame_town.scenario.blue_tank_2.state_history)
        # df_blue_state.to_excel(r'state_history.xlsx')
        # 
        # df_blue_movehistory = pd.DataFrame(B1_Move_History, B2_Move_History)
        # df_blue_movehistory.to_excel(r'move_history.xlsx')

        # # 判断一局episodes是否超过50回合
        # if wargame_town.check_rounds():
        #     first_episode_num += 1
        #     wargame_town.reset()
    # 输出算子数据到Excel_'测试1.xlsx'
    mywargame_info = {'first_episode_num': episode_num,
                      'wargame_town_steps': steps,
                      '红1坦克-高程': R1_gaochenglist,
                      '红1坦克-状态': R1_statelist,
                      '红1坦克-坐标': R1_positionlist,
                      '红2坦克-高程': R2_gaochenglist,
                      '红2坦克-状态': R2_statelist,
                      '红2坦克-坐标': R2_positionlist,
                      '蓝1坦克-高程': B1_gaochenglist,
                      '蓝1坦克-状态': B1_statelist,
                      '蓝1坦克-坐标': B1_positionlist,
                      '蓝2坦克-高程': B2_gaochenglist,
                      '蓝2坦克-状态': B2_statelist,
                      '蓝2坦克-坐标': B2_positionlist,
                      '红1坦克距夺控点距离': R1_to_obj_distancelist,
                      '红2坦克距夺控点距离': R2_to_obj_distancelist,
                      '蓝1坦克距夺控点距离': B1_to_obj_distancelist,
                      '蓝2坦克距夺控点距离': B2_to_obj_distancelist,
                      '红1蓝1坦克间距离': R1B1_distancelist,
                      '红1蓝2坦克间距离': R1B2_distancelist,
                      '红2蓝1坦克间距离': R2B1_distancelist,
                      '红2蓝2坦克间距离': R2B2_distancelist,
                      }
    df = pd.DataFrame(mywargame_info)
    df.to_excel('测试1.xlsx', index=False)

    RV.output()
    print('上半场 End')

    # --------------------上半场所对抗结束，下半场所开始-------------------------------------------------------------------
    wargame_town.change_half()
    first_record_score(wargame_town)
    wargame_town.hud.show_break_popup = True
    wargame_town.hud.show_break()
    wargame_town.steps = 0
    while second_episode_num <= second_half_episodes:
        wargame_town.render()
        wargame_town.steps += 1
        print("Second Half,episode:%s, Step:%s" % (second_episode_num, wargame_town.steps))
        wargame_town.check_indirect_fire('red')
        red_observation_, red_reward, red_done = player_2.red_choose_action(wargame_town)
        wargame_town.render()
        # 下半场的一局结束，重置
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
            if len(wargame_town.scenario.red_tank_1.action_history) < wargame_town.steps:
                wargame_town.scenario.red_tank_1.action_history.append('pass')
                wargame_town.scenario.red_tank_1.hex_history.append((0, 0))
            if len(wargame_town.scenario.red_tank_2.action_history) < wargame_town.steps:
                wargame_town.scenario.red_tank_2.action_history.append('pass')
                wargame_town.scenario.red_tank_2.hex_history.append((0, 0))

            wargame_town.check_indirect_fire('blue')
            blue_observation_, blue_reward, blue_done = player_1.blue_choose_action(wargame_town)
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
                if len(wargame_town.scenario.blue_tank_1.action_history) < wargame_town.steps:
                    wargame_town.scenario.blue_tank_1.action_history.append('pass')
                    wargame_town.scenario.blue_tank_1.hex_history.append((0, 0))
                if len(wargame_town.scenario.blue_tank_2.action_history) < wargame_town.steps:
                    wargame_town.scenario.blue_tank_2.action_history.append('pass')
                    wargame_town.scenario.blue_tank_2.hex_history.append((0, 0))
        #  判断一局episodes是否超过50回合
        # if wargame_town.check_rounds():
        #     second_episode_num += 1 nb
        #     wargame_town.reset()

    print('Second Half End')
    second_record_score(wargame_town)
    wargame_town.hud.show_end_popup = True
    wargame_town.hud.show_end()
    wargame_town.destroy()
    RV.output()

    # print('%s胜利%局 %s胜利%s局' % (
    #     wargame_town.p1_name, str(wargame_town.p1_red_win_times + wargame_town.p1_blue_win_times), wargame_town.p2_name,
    #     str(wargame_town.p2_blue_win_times + wargame_town.p2_red_win_times)))


if __name__ == '__main__':
    # wargame_town = Wargame_env()
    run_wargame(player_1, player_2)
