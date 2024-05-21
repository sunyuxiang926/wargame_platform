# 系统设定，将所有常量封装在Constants的实例变量里
# 因为用到property，故没有将其封装在类变量里


import sys

import pygame as pg
from pygame.locals import *

# 存活
class Wargame_env(object):

    # 设置无人机数量，1代表想定有无人机，可选0-4个无人机
    # UAV_list = [1, 1, 1, 1]
    UAV_list = [1, 1, 1, 1]

    def __init__(self):
        # 设置多种环境状态，每种状态下更新调试不同的场景，其中self是指出其本身的类对象
        self.caption = '【先胜1号】LZ智能战术兵棋推演平台v2.0'
        self.states = ['初始化', '人-人对抗', '人-机对抗', '机-机对抗']
        self.state = self.states[3]  # 设置当前为机-机对抗模式
        self.clock = pg.time.Clock()
        self.screen_size = [2560, 1400]
        self.fps = 60

        self.labels = pg.sprite.Group()
        self.action = None
        self.screen = None
        self.fullscreen = True
        self.total_episodes = 0
        self.red_win_times = 0
        self.blue_win_times = 0
        self.rounds = 0
        self.steps = 0

        self.red_kill_score = 0
        self.red_get_goal_score = 0
        self.red_survive_score = 0
        self.red_pointattack_score = 0
        self.red_pointdefense_score = 0
        self.red_point_flag = 0
        self.red_all_score = 0

        self.blue_kill_score = 0
        self.blue_get_goal_score = 0
        self.blue_survive_score = 0
        self.blue_pointattack_score = 0
        self.blue_pointdefense_score = 0
        self.blue_point_flag = 0
        self.blue_all_score = 0

        self.p1_name = '选手1'
        self.p2_name = '选手2'

        self.p1_red_win_times = 0
        self.p1_blue_win_times = 0

        self.p2_red_win_times = 0
        self.p2_blue_win_times = 0

        self.p1_red_kill_score = 0
        self.p1_red_get_goal_score = 0
        self.p1_red_survive_score = 0

        self.p1_blue_kill_score = 0
        self.p1_blue_get_goal_score = 0
        self.p1_blue_survive_score = 0

        self.p2_red_kill_score = 0
        self.p2_red_get_goal_score = 0
        self.p2_red_survive_score = 0

        self.p2_blue_kill_score = 0
        self.p2_blue_get_goal_score = 0
        self.p2_blue_survive_score = 0

        self.first_half = True
        self.second_half = False

        # 载入兵棋环境的各种参数，用try语句捕捉屏幕分辨率
        # 实际上是把self指向兵棋环境实例，从而方便了在对象内部实现对环境实体的调用
        # self.wargame = Wargame_env(self)
        try:
            pg.init()
            # 初始化当前窗口大小，与当前显示器分辨率一致
            self.info = pg.display.Info()
            self.screen_size = [2560, 1400]

        except:
            print('please install pygame version 1.9.3')
        # 初始化推演数据环境：窗口、菜单、想定等
        self.init_game_GUI()

        # 载入地图数据
        from terrain_editor_01.terrain import Game_map
        self.game_map = Game_map(self)
        # 初始化想定
        from scenario_editor_04.scenario_jiandi import Scenario_1
        self.scenario = Scenario_1(self, terrain=self.game_map)

        # 显示可视化窗口信息
        from platform_settings_07.hud import ToprightHud, BothsideHud, Hud
        # 人-人对抗模式下的显示界面
        self.Toprighthud = ToprightHud(self)
        # 人-机/机-机对抗模式下的显示界面
        self.Bothsidehud = BothsideHud(self)

        self.hud = Hud(self)

        # 初始化规则
        # from rule_editor_03.rule_editor import Wargame_rule
        # self.rule = Wargame_rule(self)

    @property
    def p1_win_times(self):
        return self.p1_red_win_times + self.p1_blue_win_times

    @property
    def p2_win_times(self):
        return self.p2_red_win_times + self.p2_blue_win_times

    # 检查是否推演完成100回合
    def check_rounds(self):
        # 初始化双方算子
        red = self.scenario.red_piece
        blue = self.scenario.blue_piece
        # 如果推演超过100回合没有完成夺控或歼灭，计算双方击杀得分和存活得分
        if self.steps >= 100:
            self.red_kill_score += (3 - blue.num) * 10
            self.red_survive_score += red.num * 9
            self.blue_kill_score = (3 - red.num) * 9
            self.blue_survive_score = blue.num * 10

            # 若红方击杀得分高，红方胜
            if self.red_kill_score > self.blue_kill_score:
                print('Red win, Kill Score is higher.')
                self.red_win_times += 1
                self.total_episodes += 1
                return True

            # 若蓝方击杀得分高，蓝方胜
            elif self.red_kill_score < self.blue_kill_score:
                print('Blue win, Kill Score is higher.')
                self.blue_win_times += 1
                self.total_episodes += 1
                return True

            # 若双方击杀得分一样高
            else:
                # 若红方存活得分高，红方胜
                if self.red_survive_score >= self.blue_survive_score:
                    print('Red win, Survive Score is higher.')
                    self.red_win_times += 1
                    self.total_episodes += 1
                    return True

                # 若蓝方存活得分高，蓝方胜
                elif self.red_survive_score < self.blue_survive_score:
                    print('Blue win, Survive Score is higher.')
                    self.blue_win_times += 1
                    self.total_episodes += 1
                    return True

    def check_indirect_fire(self, player):
        if self.steps <= 3:
            pass
        else:
            print(self.steps)
            if player == 'red' and self.scenario.red_tank_1.action_history[-3] == '间瞄射击':
                co_x, co_y = self.scenario.red_tank_1.hex_history[-3]
                self.judge_indirect_fire('red', co_x, co_y)
            if player == 'red' and self.scenario.red_tank_2.action_history[-3] == '间瞄射击':
                co_x, co_y = self.scenario.red_tank_2.hex_history[-3]
                self.judge_indirect_fire('red', co_x, co_y)
            if player == 'blue' and self.scenario.blue_tank_1.action_history[-3] == '间瞄射击':
                co_x, co_y = self.scenario.blue_tank_1.hex_history[-3]
                self.judge_indirect_fire('blue', co_x, co_y)
            if player == 'blue' and self.scenario.blue_tank_2.action_history[-3] == '间瞄射击':
                co_x, co_y = self.scenario.blue_tank_2.hex_history[-3]
                self.judge_indirect_fire('blue', co_x, co_y)

    def judge_indirect_fire(self, player, co_x, co_y):
        enermy_1 = None
        enermy_2 = None
        result_1 = 0
        result_2 = 0

        if player == 'red':
            if self.scenario.blue_tank_1.co_x == co_x and self.scenario.blue_tank_1.co_y == co_y:
                enermy_1 = self.scenario.blue_tank_1
            if self.scenario.blue_tank_2.co_x == co_x and self.scenario.blue_tank_2.co_y == co_y:
                enermy_2 = self.scenario.blue_tank_2
        if player == 'blue':
            if self.scenario.red_tank_1.co_x == co_x and self.scenario.red_tank_1.co_y == co_y:
                enermy_1 = self.scenario.red_tank_1
            if self.scenario.red_tank_2.co_x == co_x and self.scenario.red_tank_2.co_y == co_y:
                enermy_2 = self.scenario.red_tank_2
        if enermy_1:
            result_num = 0
            import random
            a1 = random.randint(1, 6)
            a2 = random.randint(1, 6)
            a = a1 + a2
            judge_result = None
            if a == 2 or a == 3 or a == 11 or a == 12:
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
                if b == 4 or b == 5 or b == 6 or b == 11 or b == 12: result_num = 1
                if b == 7 or b == 8 or b == 9: result_num = 0  # -1代表压制效果
                if b == 10: result_num = 2
            elif judge_result == "deviation":
                if b == 2:
                    result_num = 1
                elif b == 3 or b == 7 or b == 10 or b == 11 or b == 12:
                    result_num = 0
                else:
                    result_num = 0
            if player == 'red':
                result_1 = result_num * 9
            elif player == 'blue':
                result_1 = result_num * 10
            enermy_1.num -= result_num
            if enermy_1.num <= 0: enermy_1.num = 0
            print('%s_Indirect_Fire,Kill:' % (player), result_num, 'enermy save:', enermy_1.num)
        if enermy_2:
            result_num = 0
            import random
            a1 = random.randint(1, 6)
            a2 = random.randint(1, 6)
            a = a1 + a2
            judge_result = None
            if a == 2 or a == 3 or a == 11 or a == 12:
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
                if b == 4 or b == 5 or b == 6 or b == 11 or b == 12: result_num = 1
                if b == 7 or b == 8 or b == 9: result_num = 0  # -1代表压制效果
                if b == 10: result_num = 2
            elif judge_result == "deviation":
                if b == 2:
                    result_num = 1
                elif b == 3 or b == 7 or b == 10 or b == 11 or b == 12:
                    result_num = 0
                else:
                    result_num = 0
            if player == 'red':
                result_2 = result_num * 9
            elif player == 'blue':
                result_2 = result_num * 10
            enermy_2.num -= result_num
            if enermy_2.num <= 0: enermy_2.num = 0
            print('%s_Indirect_Fire,Kill:' % (player), result_num, 'enermy save:', enermy_2.num)

    def check_win(self):
        # 初始化双方所有算子
        red_tank_1 = self.scenario.red_tank_1
        red_tank_2 = self.scenario.red_tank_2
        red_tank_3 = self.scenario.red_tank_3
        red_tank_4 = self.scenario.red_tank_4
        red_tank_5 = self.scenario.red_tank_5
        red_tank_6 = self.scenario.red_tank_6
        red_tank_7 = self.scenario.red_tank_7
        red_tank_8 = self.scenario.red_tank_8

        if self.UAV_list[0] == 1:
            red_plane_9 = self.scenario.red_plane_9
        else:
            pass

        if self.UAV_list[1] == 1:
            red_plane_10 = self.scenario.red_plane_10
        else:
            pass

        if self.UAV_list[2] == 1:
            red_plane_11 = self.scenario.red_plane_11
        else:
            pass

        if self.UAV_list[3] == 1:
            red_plane_12 = self.scenario.red_plane_12
        else:
            pass

        blue_tank_1 = self.scenario.blue_tank_1
        blue_tank_2 = self.scenario.blue_tank_2
        blue_tank_3 = self.scenario.blue_tank_3
        blue_tank_4 = self.scenario.blue_tank_4
        blue_tank_5 = self.scenario.blue_tank_5
        blue_tank_6 = self.scenario.blue_tank_6
        blue_tank_7 = self.scenario.blue_tank_7
        blue_tank_8 = self.scenario.blue_tank_8
        blue_tank_9 = self.scenario.blue_tank_9
        blue_tank_10 = self.scenario.blue_tank_10

        # 判断双方所有算子能力值
        if red_tank_1.num <= 0:
            red_tank_1.num = 0
        if blue_tank_1.num <= 0:
            blue_tank_1.num = 0

        if red_tank_2.num <= 0:
            red_tank_2.num = 0
        if blue_tank_2.num <= 0:
            blue_tank_2.num = 0

        if red_tank_3.num <= 0:
            red_tank_3.num = 0
        if blue_tank_3.num <= 0:
            blue_tank_3.num = 0

        if red_tank_4.num <= 0:
            red_tank_4.num = 0
        if blue_tank_4.num <= 0:
            blue_tank_4.num = 0

        if red_tank_5.num <= 0:
            red_tank_5.num = 0
        if blue_tank_5.num <= 0:
            blue_tank_5.num = 0

        if red_tank_6.num <= 0:
            red_tank_6.num = 0
        if blue_tank_6.num <= 0:
            blue_tank_6.num = 0

        if red_tank_7.num <= 0:
            red_tank_7.num = 0
        if blue_tank_7.num <= 0:
            blue_tank_7.num = 0

        if red_tank_8.num <= 0:
            red_tank_8.num = 0
        if blue_tank_8.num <= 0:
            blue_tank_8.num = 0

        if blue_tank_9.num <= 0:
            blue_tank_9.num = 0
        if blue_tank_10.num <= 0:
            blue_tank_10.num = 0

        if self.UAV_list[0] == 1:
            if red_plane_9.num <= 0:
                red_plane_9.num = 0
        else:
            pass

        if self.UAV_list[1] == 1:
            if red_plane_10.num <= 0:
                red_plane_10.num = 0
        else:
            pass

        if self.UAV_list[2] == 1:
            if red_plane_11.num <= 0:
                red_plane_11.num = 0
        else:
            pass

        if self.UAV_list[3] == 1:
            if red_plane_12.num <= 0:
                red_plane_12.num = 0
        else:
            pass

        red_tank_all_num = red_tank_1.num + red_tank_2.num + red_tank_3.num + red_tank_4.num + red_tank_5.num + red_tank_6.num + red_tank_7.num + red_tank_8.num + 6
        blue_tank_all_num = blue_tank_1.num + blue_tank_2.num + blue_tank_3.num + blue_tank_4.num + blue_tank_5.num + blue_tank_6.num + blue_tank_7.num + blue_tank_8.num + blue_tank_9.num + blue_tank_10.num

        # 判断获胜条件
        # 如果小于50回合
        if self.rounds < 50:
            # 如果红方被全部歼灭,蓝方获胜
            if red_tank_all_num <= 0:
                print("Game:", self.total_episodes)
                print('Blue Win, Kill All red units')
                self.blue_win_times += 1
                self.total_episodes += 1
                self.red_survive_score += red_tank_all_num
                self.blue_survive_score += blue_tank_all_num
                return True

            # 如果蓝方被全部歼灭,红方获胜
            elif blue_tank_all_num <= 0:
                print("Game:", self.total_episodes)
                print('Red Win, Kill All blue units')
                self.red_win_times += 1
                self.total_episodes += 1
                self.red_survive_score += red_tank_all_num
                self.blue_survive_score += blue_tank_all_num
                return True
            else:
                return False

        # 如果大于50回合
        else:
            # 蓝方存活分高
            if red_tank_all_num <= blue_tank_all_num:
                print("Game:", self.total_episodes)
                print('Blue Win, Kill All red units')
                self.blue_win_times += 1
                self.total_episodes += 1
                self.red_survive_score += red_tank_all_num
                self.blue_survive_score += blue_tank_all_num
                return True

            # 红方存活分高
            else:
                print("Game:", self.total_episodes)
                print('Red Win, higher score')
                self.red_win_times += 1
                self.total_episodes += 1
                self.red_survive_score += red_tank_all_num
                self.blue_survive_score += blue_tank_all_num
                return True

    def change_half(self):
        self.second_half = not self.second_half
        self.first_half = not self.first_half

    def init_game_GUI(self):
        pg.display.init()  # 初始化
        pg.display.set_caption(self.caption)
        self.screen = pg.display.set_mode(self.screen_size)
        # self.screen = pg.display.set_mode(self.screen_size)  # 新建一个变量wargame_rec
        # self.screen_rec = self.screen.get_rect()  # 返回（top,bottom,width,height）=(0,0,1366,768)
        # print(self.screen_rec)
        # 必须初始化窗口(display.init()和set_mode())，才可以调用GFX中的图形化函数
        from resources.load_data import GFX
        pg.display.set_icon(GFX["icon"])  # 为界面设置大学校徽ICON

        from resources.load_data import FONTS
        from platform_settings_07.control_class import Label, Button, ButtonGroup
        self.buttons = ButtonGroup()
        # <editor-fold desc="显示主菜单">
        # Button((100, self.screen_rec.height / 2 - 300), self.buttons, text='地图编辑', button_size=(250, 50), font_size=40,
        #        font=FONTS['song'], fill_color=(0, 0, 255), call=self.test_function)
        # Button((100, self.screen_rec.height / 2 - 100), self.buttons, text='规则编辑', button_size=(250, 50), font_size=40,
        #        font=FONTS['song'], fill_color=(0, 0, 255), call=self.test_function)
        # Button((100, self.screen_rec.height / 2), self.buttons, text='想定编辑', button_size=(250, 50), font_size=40,
        #        font=FONTS['song'], fill_color=(0, 0, 255), call=self.test_function)
        # Button((100, self.screen_rec.height / 2 + 100), self.buttons, text='推演设置', button_size=(250, 50), font_size=40,
        #        font=FONTS['song'], fill_color=(0, 0, 255), call=self.enter_play)
        # Button((100, self.screen_rec.height / 2 + 200), self.buttons, text='指挥评估', button_size=(250, 50), font_size=40,
        #        font=FONTS['song'], fill_color=(0, 0, 255), call=self.test_function)
        # Button((100, self.screen_rec.height / 2 + 300), self.buttons, text='系统配置', button_size=(250, 50), font_size=40,
        #        font=FONTS['song'], fill_color=(0, 0, 255), call=self.test_function)
        # Button((100, self.screen_rec.height / 2 - 200), self.buttons, text='算子管理', button_size=(250, 50), font_size=40,
        #        font=FONTS['song'], fill_color=(0, 0, 255), call=self.test_function)
        # </editor-fold>
        # print(self.screen_rec.midbottom)
        # <editor-fold desc="显示口号">
        # self.wargame_slogan = Label('忠诚',
        #                             {'midbottom': (
        #                                 self.screen_rec.midbottom[0] - 300, self.screen_rec.midbottom[1] - 50)},
        #                             self.labels, font_size=60, font_path=FONTS['xx'], fill_color=(255, 0, 0))
        # self.wargame_slogan = Label('善谋',
        #                             {'midbottom': (
        #                                 self.screen_rec.midbottom[0] - 100, self.screen_rec.midbottom[1] - 50)},
        #                             self.labels, font_size=60, font_path=FONTS['xx'], fill_color=(255, 0, 0))
        # self.wargame_slogan = Label('妙算',
        #                             {'midbottom': (
        #                                 self.screen_rec.midbottom[0] + 100, self.screen_rec.midbottom[1] - 50)},
        #                             self.labels, font_size=60, font_path=FONTS['xx'], fill_color=(255, 0, 0))
        # self.wargame_slogan = Label('先胜',
        #                             {'midbottom': (
        #                                 self.screen_rec.midbottom[0] + 300, self.screen_rec.midbottom[1] - 50)},
        #                             self.labels, font_size=60, font_path=FONTS['xx'], fill_color=(255, 0, 0))
        # </editor-fold>
        self.clock = pg.time.Clock()
        self.fps = self.fps
        self.done = False

    @property
    def map_rect(self):
        return (0, 0, 3 / 4 * self.screen_size[0], self.screen_size[1])

    @property
    def hud_rect(self):
        return (3 / 4 * self.screen_size[0], 0, 1 / 4 * self.screen_size[0], self.screen_size[1])

    def event_loop(self):
        key = pg.key.get_pressed()
        self.game_map.get_key(key)
        for event in pg.event.get():
            if self.state == '初始化':
                self.get_event(event)
            self.Toprighthud.get_event(event)
            self.game_map.get_event(event)
            # self.rule.get_event(event)

            if event.type == pg.QUIT:
                print("quit")
                self.done = True
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                    sys.exit()
                # 全屏（F_Q）
                if event.key == pg.K_q:
                    print(str(event.key))
                    print(pg.display.list_modes())
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        m_screen = pg.display.set_mode(self.wargame_town.screen_size,
                                                       FULLSCREEN | HWSURFACE)  # FULLSCREEN | HWSURFACE
                    else:
                        m_screen = pg.display.set_mode((2560, 1440))
                if event.key == pg.K_0:
                    self.Bothsidehud.state_text = self.red_player.get_piece_state(self.red_player.piece)
                if event.key == pg.K_1:
                    self.Bothsidehud.state_text = self.blue_player.get_piece_state(self.blue_player.piece)

    def update(self, dt):
        self.scenario.update(dt)
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
        if self.state == '初始化':
            pass
        elif self.state == "人-人对抗":
            self.Toprighthud.update(dt)
            pass
            # print("当前推演状态为" + self.state)
        elif self.state == "人-机对抗":
            pass
            # print("当前推演状态为" + self.state)
        elif self.state == "机-机对抗":
            # print("当前推演状态为" + self.state)
            self.scenario.update(dt)

            # 在两侧显示双方对抗推演info
            self.hud.update(dt)

    def draw(self):
        # 背景填充为黑色
        self.screen.fill((0, 0, 0))
        # 推演地形绘制
        self.game_map.draw(self.screen)
        # 红蓝双方算子绘制
        self.scenario.draw(self.screen)
        # 根据不同推演设置，不同推演模式，显示不同界面
        if self.state == '初始化':
            # 绘制显示labels and buttons的GUI：屏幕左侧菜单与slogan
            self.labels.draw(self.screen)
            self.buttons.draw(self.screen)
        elif self.state == '人-人对抗':
            self.hud.draw(self.screen)
        elif self.state == '人-机对抗':
            self.labels.draw(self.screen)
            self.buttons.draw(self.screen)
            pass
        # ------------------------------------
        # 当前AI开发阶段，请在以下状态显示需要的信息
        elif self.state == '机-机对抗':
            self.labels.draw(self.screen)
            self.buttons.draw(self.screen)
            self.hud.draw(self.screen)

        pg.display.update()

    #   渲染并生成兵棋环境
    def render(self):
        dt = self.clock.tick(self.fps)
        # 交互操作
        self.event_loop()
        # 绘制并更新双方动作
        self.update(dt)
        self.draw()

    def destroy(self):
        pg.quit()

    def test_function(self, *args):
        print('hello world')

    def enter_play(self, *args):
        self.wargame.state = '推演'

    def get_event(self, event):
        self.buttons.get_event(event)

    #  重置推演环境:将算子复位到初始出发点，生命力复原
    def reset(self):
        self.scenario.update(self.clock.tick(self.fps))
        self.scenario.__init__(self, terrain=self.game_map)

        self.steps = 0
