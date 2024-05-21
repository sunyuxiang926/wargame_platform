import pygame as pg

from platform_settings_07.control_class import Label, Button, ButtonGroup
from platform_settings_07.control_class import font_surface
from resources.load_data import FONTS, GRAPHICS

suppress_sign = font_surface('S', 150, (255, 255, 255))  # 压制状态的显示标记
kill_sign = font_surface('X', 50, (255, 255, 255))  # kill状态的显示标记
num_1_sign = font_surface('1', 20, (255, 255, 255))
num_2_sign = font_surface('2', 20, (255, 255, 255))
red_indirect_sign_1 = GRAPHICS['red_122mm']
red_indirect_sign_2 = GRAPHICS['red_122mm_1']
blue_indirect_sign_1 = GRAPHICS['blue_81mm']
blue_indirect_sign_2 = GRAPHICS['blue_81mm_1']


# 平视显示器,用于显示可视化信息

# 在两边分别显示机-机/人-机红蓝双方对抗推演信息
class BothsideHud(object):
    def __init__(self, wargame):
        self.wargame_env = wargame
        self.screen_rect = pg.Surface.get_rect(self.wargame_env.screen)
        self.labels = pg.sprite.Group()
        self.Red_player_info = Label(
            "红方推演信息 %s / %s" % (self.wargame_env.red_win_times, self.wargame_env.total_episodes),
            {'topleft': (self.screen_rect[0] + 10, 100)}, self.labels, font_size=30, font_path=FONTS['song'])
        self.Blue_player_info = Label(
            "蓝方推演信息 %s / %s" % (self.wargame_env.blue_win_times, self.wargame_env.total_episodes),
            {'topleft': (self.screen_rect[2] - 400, 100)}, self.labels, font_size=30,
            font_path=FONTS['song'])
    
    def draw(self, surface):
        self.labels.draw(surface)
    
    def get_event(self, event):
        self.labels.get_event(event)
    
    def update(self, dt):
        self.labels.update(dt)
        self.Red_player_info.set_text(
            "红方推演信息 %s / %s" % (self.wargame_env.red_win_times, self.wargame_env.total_episodes))
        
        self.Blue_player_info.set_text(
            "蓝方推演信息 %s / %s" % (self.wargame_env.blue_win_times, self.wargame_env.total_episodes))


class Hud(object):
    def __init__(self, wargame):
        self.wargame_env = wargame
        self.screen_rect = pg.Surface.get_rect(pg.display.get_surface())
        screen_width_center = self.screen_rect.width / 2
        screen_height_center = self.screen_rect.height / 2
        self.up_surface = pg.Surface((self.screen_rect.width, 80))  # 创建上绘制区块大小：屏幕宽，高80pix
        self.bottom_surface = pg.Surface((self.screen_rect.width, 80))
        self.labels = pg.sprite.Group()
        self.popups = pg.sprite.Group()
        self.stage = '一'
        # 红蓝双方统计显示
        self.stage_label = Label(('第 %s 场' % self.stage), {'center': (60, 20)}, self.labels, font_size=30,
                                 text_color=(255, 255, 255), font_path=FONTS['song'], fill_color=(0, 0, 0))
        self.phase_label = Label(('第 %s 局' % self.wargame_env.total_episodes), {'center': (250, 20)}, self.labels,
                                 font_size=30, text_color=(255, 255, 255), font_path=FONTS['song'],
                                 fill_color=(0, 0, 0))
        self.red_name_label = Label(wargame.p1_name, {'center': (screen_width_center - 100, 20)}, self.labels,
                                    font_size=30, text_color=(255, 0, 0), font_path=FONTS['song'],
                                    fill_color=(0, 0, 0))
        self.blue_name_label = Label(wargame.p2_name, {'center': (screen_width_center + 100, 20)}, self.labels,
                                     font_size=30, text_color=(0, 0, 255), font_path=FONTS['song'],
                                     fill_color=(0, 0, 0))
        self.red_times_label = Label(('%s' % self.wargame_env.red_win_times),
                                     {'center': (screen_width_center - 300, 20)}, self.labels, font_size=30,
                                     text_color=(255, 255, 255), font_path=FONTS['song'], fill_color=(0, 0, 0))
        self.blue_times_label = Label(('%s' % self.wargame_env.blue_win_times),
                                      {'center': (screen_width_center + 300, 20)}, self.labels,
                                      font_size=30, text_color=(255, 255, 255), font_path=FONTS['song'],
                                      fill_color=(0, 0, 0))
        
        # -----红蓝双方各自胜负分统计-----
        #红方
        self.red_control_score_label = Label(('%s' % self.wargame_env.red_get_goal_score),
                                             {'topleft': (1280 - 5 * 200, 40)},
                                             self.labels, font_size=25,
                                             text_color=(255, 255, 255),
                                             font_path=FONTS['song'], fill_color=(255, 0, 0))
        
        self.red_kill_score_label = Label(('%s' % self.wargame_env.red_kill_score),
                                          {'topleft': (1280 - 4 * 200, 40)},
                                          self.labels, font_size=25,
                                          text_color=(255, 255, 255),
                                          font_path=FONTS['song'], fill_color=(255, 0, 0))

        self.red_survive_score_label = Label('%s' % (self.wargame_env.red_survive_score),
                                             {'topleft': (1280 - 3 * 200, 40)},
                                             self.labels, font_size=25,
                                             text_color=(255, 255, 255),
                                             font_path=FONTS['song'], fill_color=(255, 0, 0))
        self.red_pointattack_score_label = Label('%s' % (self.wargame_env.red_pointattack_score),
                                             {'topleft': (1280 - 2 * 200, 40)},
                                             self.labels, font_size=25,
                                             text_color=(255, 255, 255),
                                             font_path=FONTS['song'], fill_color=(255, 0, 0))

        self.red_pointdefense_score_label = Label('%s' % (self.wargame_env.red_pointdefense_score),
                                                 {'topleft': (1280 - 1 * 200, 40)},
                                                 self.labels, font_size=25,
                                                 text_color=(255, 255, 255),
                                                 font_path=FONTS['song'], fill_color=(255, 0, 0))

        # 蓝方
        self.blue_control_score_label = Label(('%s' % self.wargame_env.blue_get_goal_score),
                                              {'topleft': (1280, 40)},
                                              self.labels, font_size=25,
                                              text_color=(255, 255, 255),
                                              font_path=FONTS['song'], fill_color=(0, 0, 255))

        self.blue_kill_score_label = Label(('%s' % self.wargame_env.blue_kill_score),
                                           {'topleft': (1280 + 1 * 200, 40)},
                                           self.labels, font_size=25,
                                           text_color=(255, 255, 255),
                                           font_path=FONTS['song'], fill_color=(0, 0, 255))

        self.blue_survive_score_label = Label(('%s' % self.wargame_env.blue_survive_score),
                                              {'topleft': (1280 + 2 * 200, 40)},
                                              self.labels, font_size=25,
                                              text_color=(255, 255, 255),
                                              font_path=FONTS['song'], fill_color=(0, 0, 255))

        self.blue_pointattack_score_label = Label(('%s' % self.wargame_env.blue_pointattack_score),
                                              {'topleft': (1280 + 3 * 200, 40)},
                                              self.labels, font_size=25,
                                              text_color=(255, 255, 255),
                                              font_path=FONTS['song'], fill_color=(0, 0, 255))

        self.blue_pointdefense_score_label = Label(('%s' % self.wargame_env.blue_pointdefense_score),
                                              {'topleft': (1280 + 4 * 200, 40)},
                                              self.labels, font_size=25,
                                              text_color=(255, 255, 255),
                                              font_path=FONTS['song'], fill_color=(0, 0, 255))
        
        self.break_popup = Label('任意键进入下一阶段', {'center': (screen_width_center, 400)}, self.popups, font_size=30,
                                 text_color=((255, 255, 255)), font_path=FONTS['song'], fill_color=(0, 255, 0))
        
        self.show_break_popup = False
        self.show_end_popup = False

        #20210701
        self.information_label = Label('game info', {'topleft': (0, 50)},
                                              self.labels, font_size=25,
                                              text_color=(255, 255, 255),
                                              font_path=FONTS['song'])

        # 20210630
        # self.red_tank1_score_label = Label(('red tank1 %d, %d' %(self.wargame_env.scenario.red_tank_1.co_x,self.wargame_env.scenario.red_tank_1.co_y)),
        #                                       {'topleft': (0,30)},
        #                                       self.labels, font_size=15,
        #                                       text_color=(255, 255, 255),
        #                                       font_path=FONTS['song'], fill_color=(255, 0, 0))
        # self.red_tank2_score_label = Label(('red tank2 %d, %d' %(self.wargame_env.scenario.red_tank_2.co_x,self.wargame_env.scenario.red_tank_2.co_y)),
        #                                       {'topleft': (0,50)},
        #                                       self.labels, font_size=15,
        #                                       text_color=(255, 255, 255),
        #                                       font_path=FONTS['song'], fill_color=(255, 0, 0))
        # self.blue_tank1_score_label = Label(('blue tank1 %d, %d' %(self.wargame_env.scenario.red_tank_2.co_x,self.wargame_env.scenario.red_tank_2.co_y)),
        #                                       {'topleft': (screen_width_center+600,30)},
        #                                       self.labels, font_size=15,
        #                                       text_color=(255, 255, 255),
        #                                       font_path=FONTS['song'], fill_color=(0, 0, 255))
        # self.blue_tank2_score_label = Label(('blue tank2 %d, %d' %(self.wargame_env.scenario.red_tank_2.co_x,self.wargame_env.scenario.red_tank_2.co_y)),
        #                                       {'topleft': (screen_width_center+600,50)},
        #                                       self.labels, font_size=15,
        #                                       text_color=(255, 255, 255),
        #                                       font_path=FONTS['song'], fill_color=(0, 0, 255))
    
    def show_break(self):
        self.break_popup.draw(self.wargame_env.screen)
        pg.display.update()
        while self.show_break_popup:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    self.show_break_popup = False
    
    def show_end(self):
        p1_score = self.wargame_env.p1_red_kill_score + self.wargame_env.p1_blue_kill_score + self.wargame_env.p1_red_get_goal_score + self.wargame_env.p1_blue_get_goal_score + self.wargame_env.p1_red_survive_score + self.wargame_env.p1_blue_survive_score
        p2_score = self.wargame_env.p2_red_kill_score + self.wargame_env.p2_blue_kill_score + self.wargame_env.p2_red_get_goal_score + self.wargame_env.p2_blue_get_goal_score + self.wargame_env.p2_red_survive_score + self.wargame_env.p2_blue_survive_score
        
        if self.wargame_env.p1_win_times > self.wargame_env.p2_win_times:
            result = self.wargame_env.p1_name + '获胜'
            p1 = '2'
            p2 = '1'
        elif self.wargame_env.p1_win_times < self.wargame_env.p2_win_times:
            result = self.wargame_env.p2_name + '获胜'
            p1 = '1'
            p2 = '2'
        else:
            result = '平局'
            p1 = '0'
            p2 = '0'
        end_labels = pg.sprite.Group()
        end_surface = pg.Surface((300, 450))
        label_1 = Label('推演结果： ' + result, {'center': (150, 25)}, end_labels, font_size=25,
                        text_color=((255, 255, 255)), font_path=FONTS['song'], fill_color=(0, 0, 0))
        
        label_2 = Label(self.wargame_env.p1_name, {'center': (50, 75)}, end_labels, font_size=25,
                        text_color=((255, 255, 255)),
                        font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_3 = Label('统计', {'center': (150, 75)}, end_labels, font_size=25,
                        text_color=((255, 255, 255)), font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_4 = Label(self.wargame_env.p2_name, {'center': (250, 75)}, end_labels, font_size=25,
                        text_color=((255, 255, 255)), font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_5 = Label(str(self.wargame_env.p1_red_win_times), {'center': (50, 125)}, end_labels, font_size=25,
                        text_color=((255, 255, 255)),
                        font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_6 = Label('胜场数(红VS蓝)', {'center': (150, 125)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                        font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_7 = Label(str(self.wargame_env.p2_red_win_times), {'center': (250, 125)}, end_labels, font_size=25,
                        text_color=((255, 255, 255)),
                        font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_8 = Label(str(self.wargame_env.p1_blue_win_times), {'center': (50, 175)}, end_labels, font_size=25,
                        text_color=((255, 255, 255)),
                        font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_9 = Label('胜场数(蓝VS红)', {'center': (150, 175)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                        font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_10 = Label(str(self.wargame_env.p2_blue_win_times), {'center': (250, 175)}, end_labels, font_size=25,
                         text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_11 = Label(str(self.wargame_env.p1_red_kill_score + self.wargame_env.p1_blue_kill_score),
                         {'center': (50, 225)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_12 = Label("总歼敌分", {'center': (150, 225)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_13 = Label(str(self.wargame_env.p2_red_kill_score + self.wargame_env.p2_blue_kill_score),
                         {'center': (250, 225)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_14 = Label(str(self.wargame_env.p1_red_get_goal_score + self.wargame_env.p1_blue_get_goal_score),
                         {'center': (50, 275)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_15 = Label("总夺控分", {'center': (150, 275)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_16 = Label(str(self.wargame_env.p2_red_get_goal_score + self.wargame_env.p2_blue_get_goal_score),
                         {'center': (250, 275)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_17 = Label(str(self.wargame_env.p1_red_survive_score + self.wargame_env.p1_blue_survive_score),
                         {'center': (50, 325)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_18 = Label("总剩余兵力分", {'center': (150, 325)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_19 = Label(str(self.wargame_env.p2_red_survive_score + self.wargame_env.p2_blue_survive_score),
                         {'center': (250, 325)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_20 = Label(str(p1_score - p2_score), {'center': (50, 375)}, end_labels, font_size=25,
                         text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_21 = Label("净胜分", {'center': (150, 375)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_22 = Label(str(p2_score - p1_score), {'center': (250, 375)}, end_labels, font_size=25,
                         text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_23 = Label(p1, {'center': (50, 425)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_24 = Label("获胜积分", {'center': (150, 425)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        label_25 = Label(p2, {'center': (250, 425)}, end_labels, font_size=25, text_color=((255, 255, 255)),
                         font_path=FONTS['song'], fill_color=(0, 0, 0))

        end_surface.fill((50, 50, 50))
        end_labels.draw(end_surface)
        self.wargame_env.screen.blit(end_surface, (self.screen_rect.width / 2 - 150, 400))
        pg.display.update()
        while self.show_end_popup:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    self.show_end_popup = False
    
    def draw(self, surface):
        self.up_surface.fill((0, 0, 0))
        self.labels.draw(self.up_surface)
        self.bottom_surface.fill((0, 0, 0))
        surface.blit(self.up_surface, (0, 0))
        surface.blit(self.bottom_surface, (0, self.screen_rect.height - 50))
        # 绘制推演对抗轨迹
        # 红方
        # pg.draw.lines(self.wargame_env.screen, (255, 0, 0), False, self.wargame_env.scenario.red_tank_1.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (255, 0, 0), False, self.wargame_env.scenario.red_tank_2.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (255, 0, 0), False, self.wargame_env.scenario.red_tank_3.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (255, 0, 0), False, self.wargame_env.scenario.red_tank_4.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (255, 0, 0), False, self.wargame_env.scenario.red_tank_5.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (255, 0, 0), False, self.wargame_env.scenario.red_tank_6.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (255, 0, 0), False, self.wargame_env.scenario.red_tank_7.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (255, 0, 0), False, self.wargame_env.scenario.red_tank_8.trace_list, 2)

        # 蓝方
        # pg.draw.lines(self.wargame_env.screen, (0, 0, 255), False, self.wargame_env.scenario.blue_tank_1.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (0, 0, 255), False, self.wargame_env.scenario.blue_tank_2.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (0, 0, 255), False, self.wargame_env.scenario.blue_tank_3.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (0, 0, 255), False, self.wargame_env.scenario.blue_tank_4.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (0, 0, 255), False, self.wargame_env.scenario.blue_tank_5.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (0, 0, 255), False, self.wargame_env.scenario.blue_tank_6.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (0, 0, 255), False, self.wargame_env.scenario.blue_tank_7.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (0, 0, 255), False, self.wargame_env.scenario.blue_tank_8.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (0, 0, 255), False, self.wargame_env.scenario.blue_tank_9.trace_list, 2)
        # pg.draw.lines(self.wargame_env.screen, (0, 0, 255), False, self.wargame_env.scenario.blue_tank_10.trace_list, 2)

        # 绘制算子序号，在算子的左上角
        # self.wargame_env.screen.blit(num_1_sign, (self.wargame_env.scenario.red_tank_1.topleft_pix))
        # self.wargame_env.screen.blit(num_2_sign, (self.wargame_env.scenario.red_tank_2.topleft_pix))
        # self.wargame_env.screen.blit(num_1_sign, (self.wargame_env.scenario.blue_tank_1.topleft_pix))
        # self.wargame_env.screen.blit(num_2_sign, (self.wargame_env.scenario.blue_tank_2.topleft_pix))

        # 被击毙时，绘制一个X在算子上
        # if self.wargame_env.scenario.blue_tank_1.num <= 0:
        #     self.wargame_env.screen.blit(kill_sign, (self.wargame_env.scenario.blue_tank_1.topleft_pix))
        # if self.wargame_env.scenario.blue_tank_2.num <= 0:
        #     self.wargame_env.screen.blit(kill_sign, (self.wargame_env.scenario.blue_tank_2.topleft_pix))
        # if self.wargame_env.scenario.red_tank_1.num <= 0:
        #     self.wargame_env.screen.blit(kill_sign, (self.wargame_env.scenario.red_tank_1.topleft_pix))
        # if self.wargame_env.scenario.red_tank_2.num <= 0:
        #     self.wargame_env.screen.blit(kill_sign, (self.wargame_env.scenario.red_tank_2.topleft_pix))

        # 可视化直瞄射击
        # 红方
        red_tank_1 = self.wargame_env.scenario.red_tank_1
        if red_tank_1.state == '直瞄射击' and red_tank_1.enermy:
            pg.draw.line(self.wargame_env.screen, (255, 0, 0), red_tank_1.center_pix, red_tank_1.enermy.center_pix, 1)

        red_tank_2 = self.wargame_env.scenario.red_tank_2
        if red_tank_2.state == '直瞄射击' and red_tank_2.enermy:
            pg.draw.line(self.wargame_env.screen, (255, 0, 0), red_tank_2.center_pix, red_tank_2.enermy.center_pix, 1)

        red_tank_3 = self.wargame_env.scenario.red_tank_3
        if red_tank_3.state == '直瞄射击' and red_tank_3.enermy:
            pg.draw.line(self.wargame_env.screen, (255, 0, 0), red_tank_3.center_pix, red_tank_3.enermy.center_pix, 1)

        red_tank_4 = self.wargame_env.scenario.red_tank_4
        if red_tank_4.state == '直瞄射击' and red_tank_4.enermy:
            pg.draw.line(self.wargame_env.screen, (255, 0, 0), red_tank_4.center_pix, red_tank_4.enermy.center_pix, 1)

        red_tank_5 = self.wargame_env.scenario.red_tank_5
        if red_tank_5.state == '直瞄射击' and red_tank_5.enermy:
            pg.draw.line(self.wargame_env.screen, (255, 0, 0), red_tank_5.center_pix, red_tank_5.enermy.center_pix, 1)

        red_tank_6 = self.wargame_env.scenario.red_tank_6
        if red_tank_6.state == '直瞄射击' and red_tank_6.enermy:
            pg.draw.line(self.wargame_env.screen, (255, 0, 0), red_tank_6.center_pix, red_tank_6.enermy.center_pix, 1)

        red_tank_7 = self.wargame_env.scenario.red_tank_7
        if red_tank_7.state == '直瞄射击' and red_tank_7.enermy:
            pg.draw.line(self.wargame_env.screen, (255, 0, 0), red_tank_7.center_pix, red_tank_7.enermy.center_pix, 1)

        red_tank_8 = self.wargame_env.scenario.red_tank_8
        if red_tank_8.state == '直瞄射击' and red_tank_8.enermy:
            pg.draw.line(self.wargame_env.screen, (255, 0, 0), red_tank_8.center_pix, red_tank_8.enermy.center_pix, 1)

        # 蓝方
        blue_tank_1 = self.wargame_env.scenario.blue_tank_1
        if blue_tank_1.state == '直瞄射击' and blue_tank_1.enermy:
            pg.draw.line(self.wargame_env.screen, (0, 0, 255), blue_tank_1.center_pix, blue_tank_1.enermy.center_pix, 1)
        
        blue_tank_2 = self.wargame_env.scenario.blue_tank_2
        if blue_tank_2.state == '直瞄射击' and blue_tank_2.enermy:
            pg.draw.line(self.wargame_env.screen, (0, 0, 255), blue_tank_2.center_pix, blue_tank_2.enermy.center_pix, 1)

        blue_tank_3 = self.wargame_env.scenario.blue_tank_3
        if blue_tank_3.state == '直瞄射击' and blue_tank_3.enermy:
            pg.draw.line(self.wargame_env.screen, (0, 0, 255), blue_tank_3.center_pix, blue_tank_3.enermy.center_pix, 1)

        blue_tank_4 = self.wargame_env.scenario.blue_tank_4
        if blue_tank_4.state == '直瞄射击' and blue_tank_4.enermy:
            pg.draw.line(self.wargame_env.screen, (0, 0, 255), blue_tank_4.center_pix, blue_tank_4.enermy.center_pix, 1)

        blue_tank_5 = self.wargame_env.scenario.blue_tank_5
        if blue_tank_5.state == '直瞄射击' and blue_tank_5.enermy:
            pg.draw.line(self.wargame_env.screen, (0, 0, 255), blue_tank_5.center_pix, blue_tank_5.enermy.center_pix, 1)

        blue_tank_6 = self.wargame_env.scenario.blue_tank_6
        if blue_tank_6.state == '直瞄射击' and blue_tank_6.enermy:
            pg.draw.line(self.wargame_env.screen, (0, 0, 255), blue_tank_6.center_pix, blue_tank_6.enermy.center_pix, 1)

        blue_tank_7 = self.wargame_env.scenario.blue_tank_7
        if blue_tank_7.state == '直瞄射击' and blue_tank_7.enermy:
            pg.draw.line(self.wargame_env.screen, (0, 0, 255), blue_tank_7.center_pix, blue_tank_7.enermy.center_pix, 1)

        blue_tank_8 = self.wargame_env.scenario.blue_tank_8
        if blue_tank_8.state == '直瞄射击' and blue_tank_8.enermy:
            pg.draw.line(self.wargame_env.screen, (0, 0, 255), blue_tank_8.center_pix, blue_tank_8.enermy.center_pix, 1)

        blue_tank_9 = self.wargame_env.scenario.blue_tank_9
        if blue_tank_9.state == '直瞄射击' and blue_tank_9.enermy:
            pg.draw.line(self.wargame_env.screen, (0, 0, 255), blue_tank_9.center_pix, blue_tank_9.enermy.center_pix, 1)

        blue_tank_10 = self.wargame_env.scenario.blue_tank_10
        if blue_tank_10.state == '直瞄射击' and blue_tank_10.enermy:
            pg.draw.line(self.wargame_env.screen, (0, 0, 255), blue_tank_10.center_pix, blue_tank_10.enermy.center_pix, 1)

        # 可视化间瞄射击，还剩一回合以及当前回合时，采用不同的图形进行绘制。
        if self.wargame_env.steps > 2:
            if self.wargame_env.scenario.red_tank_1.action_history[-1] == '间瞄射击':
                hex = self.wargame_env.scenario.red_tank_1.hex_history[-1]
                topleft = self.wargame_env.game_map.get_topleft_from_hex(hex[0], hex[1])
                self.wargame_env.screen.blit(red_indirect_sign_1, topleft)
            if self.wargame_env.scenario.red_tank_1.action_history[-2] == '间瞄射击':
                hex = self.wargame_env.scenario.red_tank_1.hex_history[-2]
                topleft = self.wargame_env.game_map.get_topleft_from_hex(hex[0], hex[1])
                self.wargame_env.screen.blit(red_indirect_sign_2, topleft)
            
            if self.wargame_env.scenario.red_tank_2.action_history[-1] == '间瞄射击':
                hex = self.wargame_env.scenario.red_tank_2.hex_history[-1]
                topleft = self.wargame_env.game_map.get_topleft_from_hex(hex[0], hex[1])
                self.wargame_env.screen.blit(red_indirect_sign_1, topleft)
            if self.wargame_env.scenario.red_tank_2.action_history[-2] == '间瞄射击':
                hex = self.wargame_env.scenario.red_tank_2.hex_history[-2]
                topleft = self.wargame_env.game_map.get_topleft_from_hex(hex[0], hex[1])
                self.wargame_env.screen.blit(red_indirect_sign_2, topleft)
            
            if self.wargame_env.scenario.blue_tank_1.action_history[-1] == '间瞄射击':
                hex = self.wargame_env.scenario.blue_tank_1.hex_history[-1]
                topleft = self.wargame_env.game_map.get_topleft_from_hex(hex[0], hex[1])
                self.wargame_env.screen.blit(blue_indirect_sign_1, topleft)
            if self.wargame_env.scenario.blue_tank_1.action_history[-2] == '间瞄射击':
                hex = self.wargame_env.scenario.blue_tank_1.hex_history[-2]
                topleft = self.wargame_env.game_map.get_topleft_from_hex(hex[0], hex[1])
                self.wargame_env.screen.blit(blue_indirect_sign_2, topleft)
            
            if self.wargame_env.scenario.blue_tank_2.action_history[-1] == '间瞄射击':
                hex = self.wargame_env.scenario.blue_tank_2.hex_history[-1]
                topleft = self.wargame_env.game_map.get_topleft_from_hex(hex[0], hex[1])
                self.wargame_env.screen.blit(blue_indirect_sign_1, topleft)
            if self.wargame_env.scenario.blue_tank_2.action_history[-2] == '间瞄射击':
                hex = self.wargame_env.scenario.blue_tank_2.hex_history[-2]
                topleft = self.wargame_env.game_map.get_topleft_from_hex(hex[0], hex[1])
                self.wargame_env.screen.blit(blue_indirect_sign_2, topleft)
    
    def update(self, dt):
        self.stage = '上' if self.wargame_env.first_half == True else '下'
        red_mark = self.wargame_env.red_win_times
        blue_mark = self.wargame_env.blue_win_times
        
        episodes = self.wargame_env.total_episodes if self.wargame_env.first_half == True else self.wargame_env.total_episodes - 100
        self.stage_label.set_text('%s 半场' % (self.stage))
        self.phase_label.set_text('第 %s 局：' % (episodes))
        self.red_times_label.set_text('红方胜场次：%5s / %-5s' % (red_mark, episodes))  # 红方胜率统计
        self.blue_times_label.set_text('蓝方胜场次：%5s / %-5s' % (blue_mark, episodes))
        
        # 李原百修改
        self.red_control_score_label.set_text('夺控：%s' % (self.wargame_env.red_get_goal_score))
        self.blue_control_score_label.set_text('夺控：%s' % (self.wargame_env.blue_get_goal_score))

        self.red_kill_score_label.set_text('歼敌：%s' % (self.wargame_env.red_kill_score))
        self.blue_kill_score_label.set_text('歼敌：%s' % (self.wargame_env.blue_kill_score))

        self.red_survive_score_label.set_text('存活：%s' % (self.wargame_env.red_survive_score))
        self.blue_survive_score_label.set_text('存活：%s' % (self.wargame_env.blue_survive_score))

        self.red_pointattack_score_label.set_text('抢攻：%s' % (self.wargame_env.red_pointattack_score))
        self.blue_pointattack_score_label.set_text('抢攻：%s' % (self.wargame_env.blue_pointattack_score))

        self.red_pointdefense_score_label.set_text('据守：%s' % (self.wargame_env.red_pointdefense_score))
        self.blue_pointdefense_score_label.set_text('据守：%s' % (self.wargame_env.blue_pointdefense_score))

        #20210630
        # self.red_tank1_score_label.set_text(('red tank1 %d, %d' %(self.wargame_env.scenario.red_tank_1.co_x,self.wargame_env.scenario.red_tank_1.co_y)))
        # self.red_tank2_score_label.set_text(('red tank2 %d, %d' %(self.wargame_env.scenario.red_tank_2.co_x,self.wargame_env.scenario.red_tank_2.co_y)))
        # self.blue_tank1_score_label.set_text(('blue tank1 %d, %d' %(self.wargame_env.scenario.blue_tank_1.co_x,self.wargame_env.scenario.blue_tank_1.co_y)))
        # self.blue_tank2_score_label.set_text(('blue tank2 %d, %d' %(self.wargame_env.scenario.blue_tank_2.co_x,self.wargame_env.scenario.blue_tank_2.co_y)))


class PopupWindow(object):
    def __init__(self, wargame):
        self.wargame_env = wargame
    
    def draw(self, surface):
        pass
    
    def get_event(self, event):
        self.labels.get_event(event)
    
    def update(self, dt):
        self.labels.update(dt)


class LeftHud(object):
    def __init__(self, wargame):
        pass


# 在右上角显示人-人对抗推演状态信息
class ToprightHud(pg.Surface):
    def __init__(self, wargame):
        self.wargame_env = wargame
        self.r = pg.Surface.get_rect(self.wargame_env.screen)
        super(ToprightHud, self).__init__((int(self.r[2]), int(self.r[3] / 3)), pg.SRCALPHA)
        self.wargame_env.hint = None
        self.hint_text = ''
        self.state_text = ''
        self.labels = pg.sprite.Group()
        self.hint_label = Label(self.hint_text, {'topleft': (20, 0)}, self.labels, font_size=30,
                                font_path=FONTS['song'])
        self.state_label = Label(self.state_text, {'topleft': (10, 30)}, self.labels, font_size=30,
                                 font_path=FONTS['song'])
        self.buttons = ButtonGroup()
        Button((0, self.r[3] / 20 * 9), self.buttons, text='机动', button_size=(50, 20), font_size=20,
               font=FONTS['song'], fill_color=(0, 0, 255), call=self.change_to_move_state)
        Button((self.r[2] / 40 * 1.5, self.r[3] / 20 * 9), self.buttons, text='行军', button_size=(50, 20), font_size=20,
               font=FONTS['song'], fill_color=(0, 0, 255), call=self.change_to_march_state)
        Button((self.r[2] / 40 * 3, self.r[3] / 20 * 9), self.buttons, text='遮蔽', button_size=(50, 20), font_size=20,
               font=FONTS['song'], fill_color=(0, 0, 255), call=self.change_to_hide_state)
        Button((self.r[2] / 40 * 5, self.r[3] / 20 * 9), self.buttons, text='直瞄射击', button_size=(100, 20), font_size=20,
               font=FONTS['song'], fill_color=(0, 0, 255), call=self.change_to_direct_fire_state)
        Button((self.r[2] / 40 * 8, self.r[3] / 20 * 9), self.buttons, text='间瞄射击', button_size=(100, 20), font_size=20,
               font=FONTS['song'], fill_color=(0, 0, 255), call=self.change_to_indirect_fire_state)
    
    def draw(self, surface):
        self.fill((128, 128, 128, 128))
        self.labels.draw(surface)
        self.buttons.draw(surface)
        surface.blit(self, (0, 0))
        # surface.blit(self,(self.r[2]/4*3,0))
    
    def get_event(self, event):
        self.buttons.get_event(event)
    
    def update(self, dt):
        self.state_label.set_text(self.state_text)
        self.hint_label.set_text(self.hint_text)
        self.labels.update(dt)
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
    
    def change_to_move_state(self, *args):
        self.wargame_env.current_player.piece.change_to_move_state()
    
    def change_to_march_state(self, *args):
        self.wargame_env.current_player.piece.change_to_march_state()
    
    def change_to_hide_state(self, *args):
        self.wargame_env.current_player.piece.change_to_hide_state()
    
    def change_to_direct_fire_state(self, *args):
        self.wargame_env.current_player.piece.change_to_fire_state()
    
    def change_to_indirect_fire_state(self, *args):
        pass


class BottomRightHud(object):
    def __init__(self, wargame):
        pass
