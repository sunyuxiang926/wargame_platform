import pygame as pg
from resources.prepare import GFX, Screen, ButtonGroup, Button

class Title(Screen):
    def __init__(self):
        super(Title, self).__init__()
        self.bg = GFX['init_bg']
        self.make_buttons()

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.buttons.draw(surface)

    def make_buttons(self):
        #加载并显示图形化的按钮
        self.buttons = ButtonGroup()
        Button((500, 450), self.buttons, button_size=(200, 120), idle_image=GFX['01scenario_image'], call=self.jump,
               args='test')
        Button((800, 620), self.buttons, button_size=(200, 120), idle_image=GFX['03wargame_image'], call=self.jump,
               args='test')
        Button((680, 520), self.buttons, button_size=(200, 120), idle_image=GFX['05tutorial_image'], call=self.jump,
               args='test')
    def make_menue(self):
        #加载并显示文本化的按钮
        pass




    def get_event(self, event):
        self.buttons.get_event(event)

    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def jump(self, args):
        self.done = True
        self.next = args
