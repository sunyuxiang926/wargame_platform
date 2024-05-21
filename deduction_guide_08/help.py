import pygame as pg
from ..tools.load import GFX,FONTS
from ..tools.screenmanager import Screen
from ..tools.button import ButtonGroup,Button
from .. import constants as c


class Help(Screen):
    def __init__(self):
        super(Help, self).__init__()
        self.bg = GFX['推演流程']
        self.buttons = ButtonGroup()
        Button((600, 600), self.buttons, text='返回', button_size=(150, 50), font_size=40, fill_color=c.BLACK,
               font=FONTS['song'],call = self.jump,args = 'title')




    def draw(self, surface):
        surface.fill(c.CYAN)
        surface.blit(self.bg, (0,0))
        self.buttons.draw(surface)


    def get_event(self, event):
        self.buttons.get_event(event)

    def get_back(self):
        self.done = True
        self.next = 'title'

    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def jump(self,args):
        self.done = True
        self.next = args

