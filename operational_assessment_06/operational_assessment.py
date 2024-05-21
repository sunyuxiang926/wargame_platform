import numpy as np
import pygame as pg


# 红蓝双方对阵员作战效果统计类

# 红方信息统计
class RedPlayer_info(pg.sprite.Sprite):
    energy = 20

    def __init__(self, name, filename, initial_position, red_pieces=NONE):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = initial_position
        self.red_pieces = red_pieces
        self.active = False  # 红方是否是当前激活状态
        self.energy = RedPlayer_info.energy  # 红方生命力值：补击中或疲劳
        self.score = 0  # 统计红方胜分:射击对手得分+夺控要点分值
        self.level_mission = 0.0  # 任务完成程度

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()


# 蓝方信息统计
class BluePlayer_info(pg.sprite.Sprite):
    energy = 20

    def __init__(self, name, filename, initial_position, blue_pieces=NONE):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = initial_position
        self.red_pieces = blue_pieces
        self.active = False  # 蓝方是否是当前激活状态
        self.energy = BluePlayer_info.energy  # 蓝方生命力值：补击中或疲劳
        self.score = 0  # 统计蓝方胜分:射击对手得分+夺控要点分值
        self.level_mission = 0.0  # 任务完成程度

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()
