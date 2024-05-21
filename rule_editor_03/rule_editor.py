import pygame as pg

class Wargame_rule(object):
    '''
    此类设置先后手，随机数决定，设定回合时间20s
    设置红蓝双方切换
    '''

    def __init__(self, wargame):
        self.wargame_env = wargame
        self.wargame_env.current_player = None
        import random
        num = random.randint(0, 1)
        if num == 0:
            self.wargame_env.turn = 'blue'
            self.wargame_env.Toprighthud.hint_text = '蓝方先手，蓝方回合'
        else:
            self.wargame_env.turn = 'red'
            self.wargame_env.Toprighthud.hint_text = '红方先手，红方回合'

        self.timer = 20 * 1000
        self.time_counter = 0

    def get_event(self, event):
        if self.wargame_env.turn == 'red':
            self.wargame_env.red_player.get_event(event)
        elif self.wargame_env.turn == 'blue':
            self.wargame_env.blue_player.get_event(event)

    def update(self, dt):
        self.time_counter += dt
        if self.time_counter >= self.timer:
            self.time_counter -= self.timer
            self.change_turn()
        if self.wargame_env.turn == 'red':
            self.wargame_env.current_player = self.wargame_env.red_player
            self.wargame_env.Toprighthud.state_text = self.wargame_env.red_player.get_piece_state(
                self.wargame_env.red_player.piece)
        elif self.wargame_env.turn == 'blue':
            self.wargame_env.current_player = self.wargame_env.blue_player
            self.wargame_env.Toprighthud.state_text = self.wargame_env.blue_player.get_piece_state(
                self.wargame_env.blue_player.piece)

    def change_turn(self):
        if self.wargame_env.turn == 'red':
            self.wargame_env.turn = 'blue'
            self.wargame_env.blue_player.refresh()
            self.wargame_env.blue_player.do_action()
            self.wargame_env.Toprighthud.hint_text = '蓝方回合  分数' + str(self.wargame_env.blue_player.score)
        elif self.wargame_env.turn == 'blue':
            self.wargame_env.turn = 'red'
            self.wargame_env.red_player.refresh()
            self.wargame_env.red_player.do_action()
            self.wargame_env.Toprighthud.hint_text = '红方回合  分数' + str(self.wargame_env.red_player.score)

