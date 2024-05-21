import math


# 目标距离指标威胁量化
# 需要输入的参数有：t_common 坦克算子通过一格普通地形需要消耗的体力值
# t_xy 车辆通过特殊地形消耗的体力值
# d_jo 蓝方坦克J到夺控点的数量距离
# d_max 想定边界最大数量距离
# d_ij 坦克i和坦克j之间的格子距离
def target_distance_threat(t_common, t_xy, d_jo, d_max, d_ij):

    t_j_xy = (t_common / t_xy) * (1 - d_jo / d_max)
    t_i_xy = d_max - d_ij
    t_ij_xy = (t_j_xy + t_i_xy) / 2

    return t_ij_xy


# 目标速度指标威胁量化
# 需要输入的参数有：v_ij 空中目标Tj与我方评估节点Wi的相对速度大小
# v_max 目标算子的最大速度
def target_speed_threat(v_ij, v_max):

    b = 1
    t_vij = b * v_ij / v_max

    return t_vij

def target_speed_threat1(v_ij, v_max):

    b = 5
    t_vij = b * v_ij / v_max

    return t_vij

# 目标攻击指标威胁量化
# 需要输入的参数有：b 坦克算子的机动能力
# e1 坦克算子的行进间射能力 e2 坦克算子载弹能力
# e3 坦克算子的电子对抗能力 e4 坦克算子的导弹进攻能力
# dict1 以字典形式存储的坦克算子的武器系统攻击能力
# dict2 以字典形式存储的坦克算子侦查能力
def target_attract_threat(b, e1, e2, e3, e4, dict1, dict2):

    global a, d
    for key1, value1 in dict1.items():
        a = 0
        a = a + value1
    for key2, value2 in dict2.items():
        d = 0
        d = d + value2
    c = (math.log(b) + math.log(a + 1) + math.log(d + 1)) * e1 * e2 * e3 * e4

    return c

def target_attract_threat1(b, e1, e2, e3, e4, dict1, dict2):

    global a, d
    for key1, value1 in dict1.items():
        a = 0
        a = a + value1
    for key2, value2 in dict2.items():
        d = 0
        d = d + value2
    c = 5 * (math.log(b) + math.log(a + 1) + math.log(d + 1)) * e1 * e2 * e3 * e4

    return c


# 地形通视威胁量化
# 需要输入的参数有：v 直瞄射击还是间瞄射击 直瞄为0 间瞄为1
# max_h_ij 红蓝双方目标连线上的最高程
# h_j 坦克Tj所处位置的实际地形高度
# h_i 坦克Wi所处位置的实际地形高度
def topography_inter_threat(v, max_h_ij, h_j, h_i):

    global e
    t1 = 0.2
    t2 = 0.8

    f = max_h_ij-h_j

    b = max_h_ij-h_i

    if v == 0:
        if max_h_ij <= h_j & max_h_ij <= h_i:
            e = [t2, 1]
        elif max_h_ij >= h_j & max_h_ij >= h_i:
            e = [0, 0]
        elif max_h_ij >= h_j & max_h_ij <= h_i:
            e = [0, t1]
        else:
            e = [1, 1]
    if v == 1:
        e = [t1, t2]

    return e


# 环境指标量化
# 需要输入的参数有：w1 一级公路的权重向量
# w2 二级公路的权重向量
# w3 城镇居民地的权重向量
def environment_index(h1, h2, h3):

    w1 = 3
    w2 = 2
    w3 = 1
    t_e1 = w1 * h1 + w2 * h2 + w3 * h3

    return t_e1

def environment_index1(h1, h2, h3):

    w1 = 3
    w2 = 2
    w3 = 5
    t_e1 = w1 * h1 + w2 * h2 + w3 * h3

    return t_e1


# 目标防御量化
# 需要输入的参数有：armor 算子的装甲防护等级 复合装甲 重型装甲 中型装甲 轻型装甲 无装甲
def target_defense_index(armor):

    global d_j
    if armor == '复合装甲':
        d_j = 1
    elif armor == '重型装甲':
        d_j = 0.7
    elif armor == '中型装甲':
        d_j = 0.5
    elif armor == '轻型装甲':
        d_j = 0.3
    elif armor == '无装甲':
        d_j = 0

    return d_j

def target_defense_index1(armor):

    global d_j
    if armor == '复合装甲':
        d_j = 1
    elif armor == '重型装甲':
        d_j = 0.7
    elif armor == '中型装甲':
        d_j = 0.5
    elif armor == '轻型装甲':
        d_j = 0.3
    elif armor == '无装甲':
        d_j = 0

    return 5 * d_j
