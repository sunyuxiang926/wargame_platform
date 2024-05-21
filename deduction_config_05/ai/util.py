# -*- coding: utf-8 -*-
# @Time : 2021/5/12 19:48
import numpy as np


def get_state_4(wargame, tank, enemytanks):
    state = []
    state.append(tank.co_x)
    state.append(tank.co_y)
    state.append(tank.goal[0])
    state.append(tank.goal[1])
    return np.array(state)


def get_state_13(wargame, tank, enemytanks):
    state = []
    state.append(tank.co_x)
    state.append(tank.co_y)
    state.append(tank.get_piece_state()[2])  # 当前坦克血量
    state.append(tank.goal[0])  # 当前坦克目标点
    state.append(tank.goal[1])
    state.append(enemytanks[0].co_x)  # 敌方坦克1坐标
    state.append(enemytanks[0].co_y)
    state.append(enemytanks[0].get_piece_state()[2])  # 敌方坦克1血量
    state.append(tank.check_watch(enemytanks[0]))  # 是否可以看到敌方坦克1
    state.append(enemytanks[1].co_x)  # 敌方坦克2坐标
    state.append(enemytanks[1].co_y)
    state.append(enemytanks[1].get_piece_state()[2])  # 敌方坦克2血量
    state.append(tank.check_watch(enemytanks[1]))  # 是否可以看到敌方坦克2
    return np.array(state)


def replace_to_action(wargame, tank, enemytanks, state, num, px):
    out = False
    neighbor = wargame.game_map.get_neighbour(tank.co_x, tank.co_y)
    # 前6个数字为移动
    if num == 2:
        # 左上
        if tank.co_x == 10 or (tank.co_y == 5 and tank.co_x % 2 == 0):
            out = True
            return out, 0
        tank.move_one_step(neighbor[2][0], neighbor[2][1])
    elif num == 3:
        # 右上
        if tank.co_x == 10 or (tank.co_y == 45 and tank.co_x % 2 == 1):
            out = True
            return out, 0
        tank.move_one_step(neighbor[3][0], neighbor[3][1])
    elif num == 0:
        # 左
        if tank.co_y == 5:
            out = True
            return out, 0
        tank.move_one_step(neighbor[0][0], neighbor[0][1])
    elif num == 1:
        # 右
        if tank.co_y == 45:
            out = True
            return out, 0
        tank.move_one_step(neighbor[1][0], neighbor[1][1])
    elif num == 4:
        # 左下
        if tank.co_x == 25 or (tank.co_y == 5 and tank.co_x % 2 == 0):
            out = True
            return out, 0
        tank.move_one_step(neighbor[4][0], neighbor[4][1])
    elif num == 5:
        # 右下
        if tank.co_x == 25 or (tank.co_y == 45 and tank.co_x % 2 == 1):
            out = True
            return out, 0
        tank.move_one_step(neighbor[5][0], neighbor[5][1])
    # 6为射击敌方坦克1
    elif num == 6:
        result = tank.direct_fire(enemytanks[px[0]])
        return out, result
    elif num == 7:
        tank.change_to_hide_state()
        return out, 0

    return out, 0


def replace_to_action1(wargame, tank, enemytanks, state, num):
    out = False
    neighbor = wargame.game_map.get_neighbour(tank.co_x, tank.co_y)
    # 前6个数字为移动

    if num == 2:
        # 左上
        if tank.co_x == 10 or (tank.co_y == 5 and tank.co_x % 2 == 0):
            out = True
            return out, 0
        tank.move_one_step(neighbor[2][0], neighbor[2][1])

    elif num == 3:
        # 右上
        if tank.co_x == 10 or (tank.co_y == 45 and tank.co_x % 2 == 1):
            out = True
            return out, 0
        tank.move_one_step(neighbor[3][0], neighbor[3][1])

    elif num == 0:
        # 左
        if tank.co_y == 5:
            out = True
            return out, 0
        tank.move_one_step(neighbor[0][0], neighbor[0][1])

    elif num == 1:
        # 右
        if tank.co_y == 45:
            out = True
            return out, 0
        tank.move_one_step(neighbor[1][0], neighbor[1][1])

    elif num == 4:
        # 左下
        if tank.co_x == 25 or (tank.co_y == 5 and tank.co_x % 2 == 0):
            out = True
            return out, 0
        tank.move_one_step(neighbor[4][0], neighbor[4][1])

    elif num == 5:
        # 右下
        if tank.co_x == 25 or (tank.co_y == 45 and tank.co_x % 2 == 1):
            out = True
            return out, 0
        tank.move_one_step(neighbor[5][0], neighbor[5][1])

    # 6为射击敌方坦克1
    elif num == 6:
        result = tank.direct_fire(enemytanks[0])
        return out, result

    # 7为隐蔽
    elif num == 20:
        tank.change_to_hide_state()
        return out, 0

    return out, 0


def get_reward4(wargame, tank, state, state_next, out, done):
    x, y = state[0], state[1]
    x_next, y_next = state_next[0], state_next[1]
    goalx, goaly = state[2], state[3]
    distance = wargame.game_map.get_distance_between_hex(x, y, goalx, goaly)
    distance_next = wargame.game_map.get_distance_between_hex(x_next, y_next, goalx, goaly)
    reward = distance - distance_next
    # reward -= 1
    # if distance_next < distance:
    #     reward = 2
    # elif distance_next > distance:
    #     reward = -2
    # else:
    #     reward = 0
    if out:
        reward -= 4
    if done:
        reward += 10

    return reward


def get_reward13(wargame, tank, state, state_next, out, done, num1, result):
    x, y = state[0], state[1]
    num = state[2]
    type, ground = state[3], state[4]
    goalx, goaly = state[5], state[6]
    e1x, e1y = state[7], state[8]
    e1num = state[9]
    e1type, e1ground = state[10], state[11]
    see1 = state[12]
    e2x, e2y = state[13], state[14]
    e2num = state[15]
    e2type, e2ground = state[16], state[17]
    see2 = state[18]

    x_next, y_next = state_next[0], state_next[1]
    num_next = state_next[2]
    type_next, ground_next = state_next[3], state_next[4]
    # goalx, goaly = state_next[5], state_next[6]
    e1x_next, e1y_next = state_next[7], state_next[8]
    e1num_next = state_next[9]
    e1type_next, e1ground_next = state_next[10], state_next[11]
    see1_next = state_next[12]
    e2x_next, e2y_next = state_next[13], state_next[14]
    e2num_next = state_next[15]
    e2type_next, e2ground_next = state_next[16], state_next[17]
    see2_next = state_next[18]

    distance = wargame.game_map.get_distance_between_hex(x, y, goalx, goaly)
    distance_next = wargame.game_map.get_distance_between_hex(x_next, y_next, goalx, goaly)

    # 按照距目标点距离给一定奖励，但不要太大
    if distance_next < distance:
        reward = 5
    elif distance_next > distance:
        reward = -5
    else:
        reward = -1

    # 撞墙惩罚，禁止撞墙
    if out:
        reward -= 1

    # 和对抗有关的奖励
    # 没有看到而进行射击的惩罚
    if not see1 and num1 == 7:
        reward -= 10
    if not see2 and num1 == 8:
        reward -= 10
    if see1 and action == 7:
        if e1num_next == 0:
            reward += 40
        elif e1num > e1num_next:
            reward += 20

    if see2 and action == 8:
        if e2num_next == 0:
            reward += 40
        elif e2num > e2num_next:
            reward += 20

    # 被击中惩罚
    reward -= (num - num_next) * 10

    # 防止苟活
    reward -= 1

    # 蓝方胜利奖励
    if done == 1:
        reward += -40
    # 红方奖励
    elif done == 2:
        reward += 40

    return reward


def get_reward11(wargame, state, state_next, out ,result, done, p, num):
    reward = 0
    x, y = state[0], state[1]
    x_next, y_next = state_next[0], state_next[1]
    goalx, goaly = state[2], state[3]
    distance = wargame.game_map.get_distance_between_hex(x, y, goalx, goaly)
    distance_next = wargame.game_map.get_distance_between_hex(x_next, y_next, goalx, goaly)

    if distance - distance_next > 0:
        reward += 20
    else:
        reward -= 15
    if out:
        reward -= 15
    reward -= 0.005
    if num == 6:
        if result == 2:
            reward -= 5 * p[0]
        if result != 2:
            reward += 5 * p[0]
        if result == 1:
            reward += 10
    if done:
        reward = 100

    return reward


def r2_road(x, y):
    if x < 24:
        if y < 22:
            num = 5
        elif y >= 22:
            num = 4
    elif x == 24:
        if y < 22:
            num = 1
        elif y > 22:
            num = 0
    else:
        if y < 22:
            num = 3
        if y >= 22:
            num = 2

    return num
