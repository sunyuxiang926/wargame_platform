import os

import pygame as pg
from pygame.locals import *

pg.init()

def font_surface(text, size, colour):
    '''
    简单实现文字转为图层
    :param text:
    :param size:
    :param colour:
    :return:
    '''
    font = pg.font.get_default_font()
    font_layer = pg.font.Font(font, size)
    font_surface = font_layer.render(text, True, colour)
    return font_surface


class ScreenManager(object):
    '''
    管理和切换各个场景，每个场景都有各自单独的循环
    使用时 manager= {'开始画面':开始场景实例,'目录':目录实例}
    game_manager = ScreenManager()
    game_manager.setup_states('开始画面',manager)
    切换场景时通过场景里的done变量控制，通过场景的next变量切换具体下一个场景
    开始场景实例.done = True
    开始场景实例.next = '目录'
    '''

    def __init__(self):
        self.states = {}               #所有的场景放入场景字典中
        self.previous = None           #上一场景名称
        self.current = None            #当前场景名称


    def setup_states(self,start_state,state_dict):
        #初始化场景管理器，将所有场景放入，并确认当前场景
        self.current = start_state
        self.states = state_dict

    def flip_states(self,next_state):
        # 当某一场景结束时，通过其next变量指向下一场景
        p = self.states[self.current].cleanup()
        self.current = next_state
        self.states[self.current].startup(p)


    def update(self,dt):
        #保证每次只有一个场景在更新
        if self.states[self.current].done == True:
            next_state = self.states[self.current].next
            self.flip_states(next_state)
        else:
            self.states[self.current].update(dt)


    def get_event(self,event):
        #捕捉场景中的鼠标、键盘事件
        self.states[self.current].get_event(event)


    def draw(self,surface):
        #将场景在屏幕绘制
        self.states[self.current].draw(surface)


class Screen(object):
    '''
    所有场景都必须继承场景类，统一通过场景管理器进行管理
    如构建标题类，class Title(Screen)
    '''

    def __init__(self):
        # 通过persist传递场景间需要保留的数据
        # done变量控制场景是否结束
        # next变量控制指向的下一场景
        self.persist = {}
        self.done = False
        self.next = None

    def startup(self, persist):
        #场景初始化，通过persist接受上一场景参数
        self.done = False
        self.persist = persist

    def cleanup(self):
        # 场景结束，传递persist参数
        return self.persist

    def update(self):
        pass

    def get_event(self,event):
        pass



def _parse_color(color):
    '''
    可以实现pg的颜色多样化传入，如pg.Color('black'),pg.Color((0,0,0))效果都一样
    不建议使用，建议颜色统一通过其它地方查询后，放入（0，0，0）格式
    :param color:
    :return:
    '''

    if color is not None:
        try:
            return pg.Color(str(color))
        except ValueError as e:
            return pg.Color(*color)
    return color


# 字体字典，放入多个字体
LOADED_FONTS = {}

#标签控件的默认值，分别是字体路径，字号，文本颜色，填充颜色，透明度
LABEL_DEFAULTS = {
        "font_path": None,
        "font_size": 10,
        "text_color": "white", #字体，默认为白色
        "fill_color": (0, 0, 0),#菜单填充色，默认为红色
        "alpha": 255}


class _KwargMixin(object):
    '''
    用来传递多个参数，用字典形式
    各个控件继承此类，通过process_kwargs方法将参数传入各个实例中
    '''

    def process_kwargs(self, name, defaults, kwargs):
        '''

        :param name: 控件名称，'label','button'等
        :param defaults: 定义的各控件变量名称
        :param kwargs: 需要改变的参数
        :return:
        '''
        import copy     #载入copy库
        settings = copy.deepcopy(defaults) # 深复制参数名称
        for kwarg in kwargs:      # kwargs是字典，里面有多个参数
            if kwarg in settings:  #如果参数在类的参数中，进行更改
                if isinstance(kwargs[kwarg], dict):     #如果参数是字典，通过字典的更新方式
                    settings[kwarg].update(kwargs[kwarg])
                else:                                  #其余情况直接更新
                    settings[kwarg] = kwargs[kwarg]
            else:
                message = "{} has no keyword: {}"       #没有找到对应参数
                raise AttributeError(message.format(name, kwarg))
        for setting in settings:
            # 如果设置的参数少，这里将默认参数传入
            setattr(self, setting, settings[setting])

class Label(pg.sprite.Sprite, _KwargMixin):
    '''
    标签类，只在屏幕上显示文字用
    继承了Sprite类，多个标签需要通过sprite group
    '''
    def __init__(self, text, rect_attr, *groups, **kwargs):
        '''

        :param text: 需要显示的具体文字
        :param rect_attr: 背景大小，pg里的Rect
        :param groups: 需要放入group更新管理各种标签
        :param kwargs: 设置参数
        '''
        super(Label, self).__init__(*groups)                                 #构建类
        self.process_kwargs("Label", LABEL_DEFAULTS, kwargs)                  #传入参数
        path, size = self.font_path, self.font_size
        if (path, size) not in LOADED_FONTS:
            LOADED_FONTS[(path, size)] = pg.font.Font(path, size)
        self.font = LOADED_FONTS[(path, size)]
        #传入颜色
        self.fill_color = _parse_color(self.fill_color)
        self.text_color = _parse_color(self.text_color)
        #传入rect和文字
        self.rect_attr = rect_attr
        self.set_text(text)


        #设置初始文字，更新频率（如果要闪烁）
        self.original_text = self.text
        self.frequency = 500
        self.timer = 0
        self.visible = True

    def set_text(self, text):
        #设置文字
        self.text = text
        self.update_text()

    def update_text(self):
        #更新文字，如果文字有透明度，进行透明化处理
        if self.alpha != 255:
            self.fill_color = pg.Color(*[x + 1 if x < 255 else x - 1 for x in self.text_color[:3]])
        if self.fill_color:
            render_args = (self.text, True, self.text_color, self.fill_color)

        else:
            render_args = (self.text, True, self.text_color)
        #显示透明文字，通过将透明文字转换为对应的透明图片，再通过图片形式展现
        self.image = self.font.render(*render_args)
        if self.alpha != 255:
            self.image.set_colorkey(self.fill_color)
            self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(**self.rect_attr)


    def draw(self, surface):
        #将标签在屏幕上显示
        surface.blit(self.image, self.rect)


#Default values for Button objects - see Button class for specifics
#按键控件的各项参数，在类中有参数介绍
BUTTON_DEFAULTS = {
        "button_size": (128, 32),
        "call": None,
        "args": None,
        "call_on_up": True,
        "font": None,
        "font_size": 36,
        "text": None,
        "hover_text": None,
        "disable_text": None,
        "text_color": pg.Color("white"),
        "hover_text_color": None,
        "disable_text_color": None,
        "fill_color": None,
        "hover_fill_color": None,
        "disable_fill_color": None,
        "idle_image": None,
        "hover_image": None,
        "disable_image": None,
        "hover_sound": None,
        "click_sound": None,
        "visible": True,
        "active": True,
        "bindings": ()}

class ButtonGroup(pg.sprite.Group):
    """
    A sprite Group modified to allow calling each sprite in the group's
    get_event method similar to using Group.update to call each sprite's
    update method.
    与pg.sprite.Group略有不同，当Button本身不可见或者不是活动状态时，不能对其操作
    """
    def get_event(self, event, *args, **kwargs):
        check = (s for s in self.sprites() if s.active and s.visible)
        for s in check:
            s.get_event(event, *args, **kwargs)

class Button(pg.sprite.Sprite, _KwargMixin):
    """
    A clickable button which accepts a number of keyword
    arguments to allow customization of a button's
    appearance and behavior.
    与标签不同，button可以点按，点按时通过call参数调用对应函数
    """
    screen = pg.display.set_mode((1200, 700), RESIZABLE)
    _invisible = pg.Surface((1,1)).convert_alpha()
    _invisible.fill((0,0,0,0))

    def __init__(self, topleft, *groups, **kwargs):
        """
        Instantiate a Button object based on the keyword arguments. Buttons
        have three possible states (idle, hovered and disabled) and appearance
        options for each state. The button is idle when the mouse is not over
        the button and hovered when it is. The button is disabled when
        Button.active is False and will not respond to events.
        USAGE
        For buttons to function properly, Button.update must be called
        each frame/tick/update with the current mouse position and
        Button.get_event must be called for each event in the event queue.
        ARGS
        topleft: the topleft screen position of the button
        KWARGS
        Buttons accept a number of keyword arguments that may be
        passed individually, as a dict of "keyword": value pairs or a combination
        of the two. Any args that are not passed to __init__ will use the default
        values stored in the BUTTON_DEAFULTS dict
        "button_size": the size of the button in pixels 按键大小
        "call": callback function 按下按键调用的函数
        "args": args to be passed to callback function  往按下按键调用函数里传参数
        "call_on_up": set to True for clicks to occur on mouseup/keyup
                             set to False for clicks to occur on mousedown/keydown 按下响应还是松开响应
        "font": path to font - uses pg's default if None 显示字体
        "font_size": font size in pixels 字号
        "text": text to be displayed when button is idle 文本
        "hover_text": text to be displayed when mouse is over button 当鼠标在按键区域内显示文字
        "disable_text": text to be displayed when button is disabled 按键不可用时显示的文字
        "text_color": text color when button is idle   文字颜色
        "hover_text_color": text_color when mouse is hovering over button  鼠标在区域时文字颜色
        "disable_text_color": text color when button is disabled (self.active == False)  按键不可用时文字颜色
        "fill_color": button color when button is idle, transparent if None  背景填充颜色
        "hover_fill_color": button color when hovered, transparent if None  鼠标在按键区域内背景颜色
        "disable_fill_color": button color when disabled, transparent if None  按键不可用时背景颜色
        "idle_image": button image when idle, ignored if None   按键的背景图片
        "hover_image": button image when hovered, ignored if None  鼠标在按键区域时的图片
        "disable_image": button image when disabled, ignored if None  按键不可用时图片
        "hover_sound": Sound object to play when hovered, ignored if None 鼠标在按键区域时播放的音效
        "click_sound": Sound object to play when button is clicked, ignored if None 按键按下时音效
        "visible": whether the button should be drawn to the screen 按键可见
        "active": whether the button should respond to events 按键被激活
        "bindings": which buttons, if any, should be able to click the button - values should
                         be a sequence of pg key constants, e.g, (pg.K_UP, pg.K_w)
        """
        super(Button, self).__init__(*groups)
        color_args = ("text_color", "hover_text_color", "disable_text_color",
                           "fill_color", "hover_fill_color", "disable_fill_color")
        for c_arg in color_args:
            if c_arg in kwargs and kwargs[c_arg] is not None:
                 kwargs[c_arg] = _parse_color(kwargs[c_arg])
        self.process_kwargs("Button", BUTTON_DEFAULTS, kwargs)
        self.rect = pg.Rect(topleft, self.button_size)
        rendered = self.render_text()
        self.idle_image = self.make_image(self.fill_color, self.idle_image,
                                          rendered["text"])
        self.hover_image = self.make_image(self.hover_fill_color,
                                           self.hover_image, rendered["hover"])
        self.disable_image = self.make_image(self.disable_fill_color,
                                             self.disable_image,
                                             rendered["disable"])
        self.image = self.idle_image
        self.clicked = False
        self.hover = False

    def render_text(self):
        """Render text for each button state.
        切换不同状态下按键的文字情况
        """
        font, size = self.font, self.font_size
        if (font, size) not in LOADED_FONTS:
            LOADED_FONTS[font, size] = pg.font.Font(font, size)
        self.font = LOADED_FONTS[font, size]
        text = self.text and self.font.render(self.text, 1, self.text_color)
        hover = self.hover_text and self.font.render(self.hover_text, 1,
                                                     self.hover_text_color)
        disable = self.disable_text and self.font.render(self.disable_text, 1,
                                                       self.disable_text_color)
        return {"text": text, "hover": hover, "disable": disable}

    def make_image(self, fill, image, text):
        """
        Create needed button images.
        图片填充按键
        """
        if not any((fill, image, text)):
            return None
        final_image = pg.Surface(self.rect.size).convert_alpha()
        final_image.fill((0,0,0,0))
        rect = final_image.get_rect()
        fill and final_image.fill(fill, rect)
        image and final_image.blit(image, rect)
        text and final_image.blit(text, text.get_rect(center=rect.center))
        return final_image

    def get_event(self, event):
        """Process events.
        捕捉pg的事件
        """
        if self.active and self.visible:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.on_up_event(event)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.on_down_event(event)
            elif event.type == pg.KEYDOWN and event.key in self.bindings:
                self.on_down_event(event, True)
            elif event.type == pg.KEYUP and event.key in self.bindings:
                self.on_up_event(event, True)

    def on_up_event(self, event, onkey=False):
        """
        Process mouseup and keyup events.
        按键按下后松开，播放按键声音，同时调用相应函数，与on_down_event一样，仅时效不同
        """
        if self.clicked and self.call_on_up:
            self.click_sound and self.click_sound.play()
            self.call and self.call(self.args or self.text)
        self.clicked = False

    def on_down_event(self, event, onkey=False):
        """
        Process mousedown and keydown events.
        按键被按下，播放按键声音，同时调用相应的函数
        """
        if self.hover or onkey:
            self.clicked = True
            if not self.call_on_up:

                self.click_sound and self.click_sound.play()
                self.call and self.call(self.args or self.text)

    def update(self, prescaled_mouse_pos):
        """
        Determine whehter the mouse is over the button and
        change button appearance if necessary. Calling
        ButtonGroup.update will call update on any Buttons
        in the group.
        更新，检测按键是否可见，鼠标是否在按键上方
        """
        hover = self.rect.collidepoint(prescaled_mouse_pos)    #检查鼠标位置
        pressed = pg.key.get_pressed()                         #检查键盘的按下情况
        if any(pressed[key] for key in self.bindings):         #鼠标位置在按键上方时激活
            hover = True
        if not self.visible:                                   #按键不可见时
            self.image = Button._invisible
        elif self.active:                                          #按键可见且激活状态
            self.image = (hover and self.hover_image) or self.idle_image
            if not self.hover and hover:
                self.hover_sound and self.hover_sound.play()            #播放对应声音
            self.hover = hover
        else:
            self.image = self.disable_image or self.idle_image

    def draw(self, surface):
        """
        Draw the button to the screen.
        将按键在屏幕显示
        """
        surface.blit(self.image, self.rect)


# 键盘对象类
class Keyboard(object):
    def __init__(self, delt_x=8, delt_y=8):
        # 键盘事件
        self.k_left_down = False  # 标识左方向键是否按下
        self.k_right_down = False  # 标识右方向键是否按下
        self.k_up_down = False  # 标识向上方向键是否按下
        self.k_down_down = False  # 标识向下方向键是否按下
        self.k_space_down = False  # 标识空格键是否按下
        self.k_space_click = False
        self.K_r_down = False  # 标识R键是否按下
        self.K_e_down = False  # 标识E键是否按下
        self.fullscreen = False
        self.screen = pg.display.get_surface()

        # 每个键盘事件的偏移量
        self.delt_x = delt_x  # 键盘事件一次的x轴的偏移量
        self.delt_y = delt_y  # 键盘事件一次的y轴的偏移量

    # 接受键盘事件
    def key_event_handling(self):
        # -------进入鼠标与键盘交互事件序列-----------------
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.k_left_down = True
                elif event.key == K_RIGHT:
                    self.k_right_down = True
                elif event.key == K_UP:
                    self.k_up_down = not k_up_down
                elif event.key == K_DOWN:
                    self.k_down_down = not k_down_down
                elif event.key == K_f:
                    self.FIRE = True
                elif event.key == K_r:  # 改变棋子射击方向rotation_angle
                    self.K_r_down = True
                elif event.key == K_e:  # 改变棋子射击方向rotation_angle
                    self.K_e_down = True
                elif event.key == K_SPACE:
                    self.k_space_down = True
                elif event.key == K_F12:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        pg.display.set_mode((2560, 1440), FULLSCREEN | HWSURFACE, 32)
                        SCREEN_WIDTH2, SCREEN_HEIGHT2 = (2560, 1440)
                    else:
                        pg.display.set_mode(bg_size1)
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    self.k_left_down = False
                elif event.key == K_RIGHT:
                    self.k_right_down = False
                elif event.key == K_UP:
                    self.k_up_down = False
                elif event.key == K_DOWN:
                    self.k_down_down = False
                elif event.key == K_f:
                    pass
                elif event.key == K_r:
                    self.K_r_down = False
                elif event.key == K_e:
                    self.K_e_down = False
                elif event.key == K_SPACE:
                    self.k_space_click = True

# 鼠标精灵类（利用pg.sprite模块）
class Mouse(pg.sprite.Sprite):
    """鼠标的属性与事件处理"""
    def __init__(self, filename, scenario, initial_position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect() #抓取的图像
        self.rect.center = initial_position
        self.screen = pg.display.get_surface()
        self.mask = pg.mask.from_surface(self.image)
        # 鼠标事件
        self.Mouse_left_click = False
        self.Mouse_right_click = False #标识鼠标右键点击
        self.Mouse_middle_click = False
        self.Mouse_mid_click = False #中键
        self.Mouse_mid_forward = False #中键向前
        self.Mouse_mid_backward = False #中键向后
        self.Mouse_drag_measure = 0  # 标识鼠标测量，未拖拽状态;1：拖拽中;2：已完成
        self.Mouse_drag_map = 0  # 标识鼠标拖放地图，未拖拽状态;1：拖拽中;2：已完成
        self.Mouse_event_on = False #标识某一事件打开or关闭
        self.Mouse_left_down = False #标识鼠标左键被按下的状态
        self.Mouse_right_down = False

        self.GUI_state = -1 # 标识现在的游戏阶段
        self.indirect_state = -1 # 标识间瞄阶段的小阶段

        #  self.Last_red_piece =   # 选中的上一个红方棋子
        #  self.Last_blue_piece =   # 选中的上一个蓝方棋子

        # 位置初始化
        self.pos_start = [0, 0]  # 鼠标选择的起点
        self.pos_stop = [0, 0]  # 鼠标选择的终点


        # 部署阶段的辅助变量
        self.pos_click = [0, 0]
        self.piece_choise = False  # 是否有红方棋子被选中，用于防止红蓝棋子叠在一起时难以分开


        #机动阶段的辅助变量
        self.last_piece = Piece("red_T62", (-1, -1), NONE, (1360, 700)) # 上一个选中的棋子
        self.last_hex = Hexagon("mapAh", -1, (-1000, -1000), -100, NONE)  # 上一个选中的六角格
        self.piece_move_point = 0 #当前棋子的机动值
        self.Red_move = True # 暂设为红方先行
        self.click_pos = [-1000, -1000]  # 存储上一个点击的位置
        self.hex_list = [] # 队列存储机动路线
        self.line_list = [] # 路线用存储列表

        #直瞄射击阶段的辅助变量
        self.shot_piece = Piece("red_T62", (-1, -1), NONE, (1360, 700)) # 进行射击的棋子
        self.goal_piece = Piece("red_T62", (-1, -1), NONE, (1360, 700)) # 射击目标棋子
        self.shot_hex = Hexagon("mapAh", -1, (-1000, -1000), -100, NONE) # 射击棋子所在六角格
        self.goal_hex = Hexagon("mapAh", -1, (-1000, -1000), -100, NONE) # 目标棋子所在六角格
        self.Red_shot = True # 暂设为红方先射击
        self.shoot_sound = pg.mixer.Sound("sound/shoot.wav")
        self.shoot_sound.set_volume(0.8)

        # 鼠标点选的对象
        self.scenario = scenario
        self.red_pieces = scenario.red_pieces
        self.blue_pieces = scenario.blue_pieces
        self.piece_group = scenario.piece_group
        self.hex_group = scenario.terrain.hexagon_group

    def distanse(self, shot_hex, goal_hex):  # 距离测量
        self.shot_row = int(shot_hex.ID) // 100
        self.shot_col = int(shot_hex.ID) % 100
        self.goal_row = int(goal_hex.ID) // 100
        self.goal_col = int(goal_hex.ID) % 100
        if self.shot_row % 2 == 0:
            if self.goal_col >= self.shot_col:
                if self.goal_row >= self.shot_row:
                    rev = (self.goal_row + 1 - self.shot_row) // 2  # 修正值
                    self.goal_col = self.goal_col - rev
                    dis = ((self.goal_row - self.shot_row) + (self.goal_col - self.shot_col)) * 50
                else:
                    rev = (self.shot_row - self.goal_row) // 2
                    self.goal_col = self.goal_col - rev
                    dis = ((self.shot_row - self.goal_row) + (self.goal_col - self.shot_col)) * 50

            else:
                if self.shot_row >= self.goal_row:
                    rev = (self.shot_row + 1 - self.goal_row) // 2  # 修正值
                    self.shot_col = self.shot_col - rev
                    dis = ((self.shot_row - self.goal_row) + (self.shot_col - self.goal_col)) * 50
                else:
                    rev = (self.goal_row - self.shot_row) // 2
                    self.shot_col = self.shot_col - rev
                    dis = ((self.goal_row - self.shot_row) + (self.shot_col - self.goal_col)) * 50

        else:
            if self.goal_col >= self.shot_col:
                if self.goal_row >= self.shot_row:
                    rev = (self.goal_row - self.shot_row) // 2  # 修正值
                    self.goal_col = self.goal_col - rev
                    dis = ((self.goal_row - self.shot_row) + (self.goal_col - self.shot_col)) * 50
                else:
                    rev = (self.shot_row + 1 - self.goal_row) // 2
                    self.goal_col = self.goal_col - rev
                    dis = ((self.shot_row - self.goal_row) + (self.goal_col - self.shot_col)) * 50

            else:
                if self.shot_row >= self.goal_row:
                    rev = (self.shot_row + 1 - self.goal_row) // 2  # 修正值
                    self.shot_col = self.shot_col - rev
                    dis = ((self.shot_row - self.goal_row) + (self.shot_col - self.goal_col)) * 50
                else:
                    rev = (self.goal_row - self.shot_row) // 2
                    self.shot_col = self.shot_col - rev
                    dis = ((self.goal_row - self.shot_row) + (self.shot_col - self.goal_col)) * 50

        return dis

    # 规则模块：机动、侦察、直瞄射击、间瞄射击规则等
    # 蓝对红方射击效果裁决
    def Effectiveness_bluetored(self, firing_unit, target_unit, range, landform, Dice_roll, goal_piece):
        spe_event = 0 # 特殊情况:1为遮障中的APC，2为遮障中的Tank
        result = ""
        Attack_Rating = 0
        #TODO:---美军火力单位对苏军车辆攻击效果评价表：combat result table,CRT
        if firing_unit == "LAW" and target_unit == "Tank" or target_unit =="APC":
            if range <= 50:
                Attack_Rating = 8
            elif 50 < range <= 100:
                Attack_Rating = 7
            elif 100 < range <= 150:
                Attack_Rating = 5
            elif 150 < range <= 200:
                Attack_Rating = 3
            elif 200 < range <= 250:
                Attack_Rating = 2
            elif 250 < range <= 400:
                Attack_Rating = 1
            elif 400 < range:
                Attack_Rating = 0
        if firing_unit == "DRAGON" and target_unit == "Tank" or target_unit =="APC":
            if range <= 50:
                Attack_Rating = 0
            elif 50 < range <= 100:
                Attack_Rating = 4
            elif 100 < range <= 150:
                Attack_Rating = 8
            elif 150 < range <= 1000:
                Attack_Rating = 9
            elif 1000 < range:
                Attack_Rating = 0
        if firing_unit == "TOW" and target_unit == "Tank" or target_unit =="APC":
            if range <= 100:
                Attack_Rating = 0
            elif 100 < range <= 150:
                Attack_Rating = 5
            elif 150 < range <= 200:
                Attack_Rating = 8
            elif 200 < range <= 3000:
                Attack_Rating = 9
            else:
                Attack_Rating = 0
        if firing_unit == "M60A1" and target_unit == "Tank":
            if range <= 100:
                Attack_Rating = 10
            elif 100 < range <= 500:
                Attack_Rating = 9
            elif 500 < range <= 750:
                Attack_Rating = 8
            elif 750 < range <= 1000:
                Attack_Rating = 7
            elif 1000 < range <= 1500:
                Attack_Rating = 6
            elif 1500 < range <= 2000:
                Attack_Rating = 4
            elif 2000 < range <= 2500:
                Attack_Rating = 3
            elif 2500 < range <= 3000:
                Attack_Rating = 2
            else:
                Attack_Rating = 0
        if firing_unit == "M60A1" and target_unit == "APC":
            if range <= 1000:
                Attack_Rating = 8
            elif 1000 < range <= 1500:
                Attack_Rating = 5
            elif 1500 < range <= 2000:
                Attack_Rating = 4
            elif 2000 < range <= 3000:
                Attack_Rating = 2
            else:
                Attack_Rating = 0
        if firing_unit == "M60A2_gun" and target_unit == "Tank":
            if range <= 750:
                Attack_Rating = 9
            elif 750 < range <= 1000:
                Attack_Rating = 7
            elif 1000 < range <= 1500:
                Attack_Rating = 5
            elif 1500 < range <= 2000:
                Attack_Rating = 3
            else:
                Attack_Rating = 0
        if firing_unit == "M60A2_gun" and target_unit == "APC":
            if range <= 500:
                Attack_Rating = 10
            elif 500 < range <= 1000:
                Attack_Rating = 9
            elif 1000 < range <= 1500:
                Attack_Rating = 8
            elif 1500 < range <= 2000:
                Attack_Rating = 5
            elif 2000 < range <= 2500:
                Attack_Rating = 3
            elif 2500 < range <= 3000:
                Attack_Rating = 1
            else:
                Attack_Rating = 0
        if firing_unit == "M60A2_msl" and target_unit == "Tank":
            if 450 < range <= 3000:
                Attack_Rating = 10
            else:
                Attack_Rating = 0
        if firing_unit == "M60A2_msl" and target_unit == "APC":
            if 450 < range <= 3000:
                Attack_Rating = 11
            else:
                Attack_Rating = 0
        if firing_unit == "M60A3" and target_unit == "Tank":
            if range <= 750:
                Attack_Rating = 10
            elif 750 < range <= 1000:
                Attack_Rating = 9
            elif 1000 < range <= 1500:
                Attack_Rating = 8
            elif 1500 < range <= 2000:
                Attack_Rating = 7
            elif 2000 < range <= 2500:
                Attack_Rating = 6
            elif 2500 < range <= 3000:
                Attack_Rating = 5
            else:
                Attack_Rating = 0
        if firing_unit == "M60A3" and target_unit == "APC":
            if range <= 500:
                Attack_Rating = 9
            elif 500 < range <= 1000:
                Attack_Rating = 8
            elif 1000 < range <= 1500:
                Attack_Rating = 7
            elif 1500 < range <= 2500:
                Attack_Rating = 5
            elif 2500 < range <= 3000:
                Attack_Rating = 4
            else:
                Attack_Rating = 0
        if firing_unit == "XM1" and target_unit == "Tank":
            if range <= 1500:
                Attack_Rating = 10
            elif 1500 < range <= 3000:
                Attack_Rating = 8
            else:
                Attack_Rating = 0
        if firing_unit == "XM1" and target_unit == "APC":
            if range <= 1500:
                Attack_Rating = 10
            elif 1500 < range <= 2000:
                Attack_Rating = 9
            elif 2000 < range <= 2500:
                Attack_Rating = 8
            elif 2500 < range <= 3000:
                Attack_Rating = 6
            else:
                Attack_Rating = 0
        if firing_unit == "MICV" and target_unit == "Tank":
            if range <= 500:
                Attack_Rating = 4
            else:
                Attack_Rating = 0
        if firing_unit == "MICV" and target_unit == "APC":
            if range <= 1000:
                Attack_Rating = 7
            elif 1000 < range <= 1500:
                Attack_Rating = 6
            elif 1500 < range <= 2000:
                Attack_Rating = 5
            else:
                Attack_Rating = 0
        if target_unit == "APC" and landform == " 遮  障":
            spe_event = 1
        if target_unit == "Tank" and landform == " 遮  障":
            spe_event = 2

        if target_unit == "Tank" or target_unit =="APC": # 归类
            target_unit = "vehicle_combatant"

        # TODO:---美军火力单位对苏军人员攻击效果评价表：combat result table,CRT
        if  target_unit == "soveit_combatant":
            if firing_unit == "TM+":
                if range <= 200:
                    Attack_Rating = 8
                elif 200 < range <= 300:
                    Attack_Rating = 7
                elif 300 < range <= 350:
                    Attack_Rating = 6
                elif 350 < range <= 400:
                    Attack_Rating = 5
                elif 400 < range <= 450:
                    Attack_Rating = 4
                elif 450 < range <= 500:
                    Attack_Rating = 3
                elif 500 < range <= 1000:
                    Attack_Rating = 2
                else:
                    Attack_Rating = 0
            if firing_unit == "TM":
                if range <= 200:
                    Attack_Rating = 7
                elif 200 < range <= 300:
                    Attack_Rating = 6
                elif 300 < range <= 350:
                    Attack_Rating = 5
                elif 350 < range <= 400:
                    Attack_Rating = 4
                elif 400 < range <= 450:
                    Attack_Rating = 2
                elif 450 < range <= 500:
                    Attack_Rating = 1
                else:
                    Attack_Rating = 0
            if firing_unit == "MG":
                if range <= 500:
                    Attack_Rating = 3
                elif 500 < range <= 1000:
                    Attack_Rating = 2
                else:
                    Attack_Rating = 0
            if firing_unit == "TM+" or firing_unit == "M113":
                if range <= 500:
                    Attack_Rating = 4
                elif 500 < range <= 1000:
                    Attack_Rating = 3
                elif 1000 < range <= 2000:
                    Attack_Rating = 2
                else:
                    Attack_Rating = 0
            if firing_unit == "M60A1" or firing_unit == "M60A2_gun" or firing_unit == "M60A2_msl" or firing_unit == "M60A3":
                if range <= 100:
                    Attack_Rating = 4
                elif 100 < range <= 500:
                    Attack_Rating = 5
                elif 500 < range <= 1500:
                    Attack_Rating = 4
                elif 1500 < range <= 2000:
                    Attack_Rating = 3
                elif 2000 < range <= 2500:
                    Attack_Rating = 2
                else:
                    Attack_Rating = 0
            if firing_unit == "XM1":
                if range <= 2000:
                    Attack_Rating = 7
                elif 2000 < range <= 3000:
                    Attack_Rating = 5
                else:
                    Attack_Rating = 0
            if firing_unit == "MICV":
                if range <= 500:
                    Attack_Rating = 8
                elif 500 < range <= 1000:
                    Attack_Rating = 7
                elif 1000 < range <= 2000:
                    Attack_Rating = 5
                elif 2000 < range <= 3000:
                    Attack_Rating = 3
                else:
                    Attack_Rating = 0

        goal_piece.direct_rating = Attack_Rating

        # ---------反车辆战斗结果表----------------------------------------
        if target_unit == "vehicle_combatant":  # 攻击车辆时

            if Dice_roll == 2:
                if 1 <= Attack_Rating <= 8:      result = "kf"
                if 9 <= Attack_Rating <= 11: result = "k"
            if Dice_roll == 3:
                if 1 <= Attack_Rating <= 2:      result = "no_effect"
                if 3 <= Attack_Rating <= 11: result = "k"
            if Dice_roll == 4:
                if 1 <= Attack_Rating <= 4:      result = "no_effect"
                if 5 <= Attack_Rating <= 11: result = "k"
            if Dice_roll == 5:
                if 1 <= Attack_Rating <= 6:      result = "no_effect"
                if 7 <= Attack_Rating <= 11: result = "k"
            if Dice_roll == 6:
                if 1 <= Attack_Rating <= 8:      result = "no_effect"
                if 9 <= Attack_Rating <= 11: result = "k"
            if Dice_roll == 7:
                if 1 <= Attack_Rating <= 10:     result = "no_effect"
                if Attack_Rating == 11:      result = "k"
            if Dice_roll == 8:
                if 1 <= Attack_Rating <= 9:      result = "no_effect"
                if 10 <= Attack_Rating <= 11: result = "k"
            if Dice_roll == 9:
                if 1 <= Attack_Rating <= 7:      result = "no_effect"
                if 8 <= Attack_Rating <= 11: result = "k"
            if Dice_roll == 10:
                if 1 <= Attack_Rating <= 5:      result = "no_effect"
                if 6 <= Attack_Rating <= 11: result = "k"
            if Dice_roll == 11:
                if 1 <= Attack_Rating <= 3:      result = "no_effect"
                if 4 <= Attack_Rating <= 11: result = "k"
            if Dice_roll == 12:
                if Attack_Rating == 1:      result = "no_effect"
                if 4 <= Attack_Rating <= 11: result = "km"
            # ------特殊地形情况----------
            if landform == " 城  镇":
                if Dice_roll == 2:
                    result = "no_effect"
            if landform == " 森  林":
                if Dice_roll == 3 or 4:
                    result = "no_effect"
            if spe_event == 1:
                if Dice_roll >= 5:
                    result = "no_effect"
            if spe_event == 2:
                if Dice_roll >= 7:
                    result = "no_effect"

        if target_unit == "Soviet_combatant":  # 攻击人员时
            if Dice_roll == 2:
                if 1 <= Attack_Rating <= 3:
                    result = "s"
                if 4 <= Attack_Rating <= 9:
                    result = "k"
            if Dice_roll == 3:
                if 1 <= Attack_Rating <= 1:
                    result = "no_effect"
                if 2 <= Attack_Rating <= 4:
                    result = "s"
                if 5 <= Attack_Rating <= 9:
                    result = "k"
            if Dice_roll == 4:
                if 1 <= Attack_Rating <= 3:
                    result = "no_effect"
                if 4 <= Attack_Rating <= 7:
                    result = "s"
                if 8 <= Attack_Rating <= 9:
                    result = "k"
            if Dice_roll == 5:
                if 1 <= Attack_Rating <= 4:
                    result = "no_effect"
                if 5 <= Attack_Rating <= 9:
                    result = "s"
            if Dice_roll == 6:
                if 1 <= Attack_Rating <= 5:
                    result = "no_effect"
                if 6 <= Attack_Rating <= 9:
                    result = "s"
            if Dice_roll == 7:
                if 1 <= Attack_Rating <= 6:
                    result = "no_effect"
                if 7 <= Attack_Rating <= 9:
                    result = "s"
            if Dice_roll == 8:
                if 1 <= Attack_Rating <= 6:
                    result = "no_effect"
                if 7 <= Attack_Rating <= 9:
                    result = "s"
            if Dice_roll == 9:
                if 1 <= Attack_Rating <= 5:
                    result = "no_effect"
                if 6 <= Attack_Rating <= 9:
                    result = "s"
            if Dice_roll == 10:
                if 1 <= Attack_Rating <= 4:
                    result = "no_effect"
                if 5 <= Attack_Rating <= 8:
                    result = "s"
                if Attack_Rating == 9:
                    result = "k"
            if Dice_roll == 11:
                if 1 <= Attack_Rating <= 2:
                    result = "no_effect"
                if 3 <= Attack_Rating <= 7:
                    result = "s"
                if 8 <= Attack_Rating <= 9:
                    result = "k"
            if Dice_roll == 12:
                if 1 <= Attack_Rating <= 6:
                    result = "s"
                if 7 <= Attack_Rating <= 9:
                    result = "k"

            # ---------特殊地形情况---------
            if landform == " 城  镇" or landform ==" 森  林":
                if Dice_roll <= 4:
                    result = "no_effect"
            if landform == " 遮  障":
                if Dice_roll >= 7:
                    result = "no_effect"
        return result

    def Effectiveness_redtoblue(self, firing_unit, target_unit, range, landform, Dice_roll, goal_piece):
        # result = judge_fight_result(firing_unit, target_unit, range)
        # return result
        result = ""
        Attack_Rating = 0
        spe_event = 0 # 特殊情况:1为遮障中的APC，2为遮障中的Tank
        # ----苏军火力单位对美军车辆攻击效果评价表：combat result table,CRT
        if firing_unit == "RPG7" and target_unit == "Tank":
            if range <= 50:
                Attack_Rating = 8
            elif 50 < range <= 100:
                Attack_Rating = 7
            elif 100 < range <= 150:
                Attack_Rating = 6
            elif 150 < range <= 200:
                Attack_Rating = 5
            elif 200 < range <= 300:
                Attack_Rating = 3
            elif 300 < range <= 400:
                Attack_Rating = 2
            elif 400 < range <= 500:
                Attack_Rating = 1
            else:
                Attack_Rating = 0
        if firing_unit == "RPG7" and target_unit == "APC":
            if range <= 50:
                Attack_Rating = 9
            elif 50 < range <= 100:
                Attack_Rating = 8
            elif 100 < range <= 150:
                Attack_Rating = 7
            elif 150 < range <= 200:
                Attack_Rating = 6
            elif 200 < range <= 350:
                Attack_Rating = 4
            elif 350 < range <= 400:
                Attack_Rating = 3
            elif 400 < range <= 500:
                Attack_Rating = 2
            else:
                Attack_Rating = 0
        if firing_unit == "SPG9" and target_unit == "Tank":
            if range <= 300:
                Attack_Rating = 8
            elif 300 < range <= 500:
                Attack_Rating = 7
            elif 500 < range <= 750:
                Attack_Rating = 6
            elif 750 < range <= 1000:
                Attack_Rating = 4
            else:
                Attack_Rating = 0
        if firing_unit == "SPG9" and target_unit == "APC":
            if range <= 200:
                Attack_Rating = 8
            elif 200 < range <= 500:
                Attack_Rating = 7
            elif 500 < range <= 1000:
                Attack_Rating = 6
            else:
                Attack_Rating = 0
        if firing_unit == "T62" and target_unit == "Tank":
            if range <= 200:
                Attack_Rating = 10
            elif 200 < range <= 750:
                Attack_Rating = 9
            elif 750 < range <= 1000:
                Attack_Rating = 8
            elif 1000 < range <= 1500:
                Attack_Rating = 7
            elif 1500 < range <= 2000:
                Attack_Rating = 6
            elif 2000 < range <= 2500:
                Attack_Rating = 4
            elif 2500 < range <= 3000:
                Attack_Rating = 2
            else:
                Attack_Rating = 0
        if firing_unit == "T62" and target_unit == "APC":
            if range <= 750:
                Attack_Rating = 9
            elif 750 < range <= 1000:
                Attack_Rating = 8
            elif 1000 < range <= 1500:
                Attack_Rating = 6
            elif 1500 < range <= 2000:
                Attack_Rating = 4
            elif 2000 < range <= 2500:
                Attack_Rating = 3
            elif 2500 < range <= 3000:
                Attack_Rating = 2
            else:
                Attack_Rating = 0
        if firing_unit == "BMP_gun" and target_unit == "Tank":
            if range <= 300:
                Attack_Rating = 8
            elif 300 < range <= 450:
                Attack_Rating = 7
            elif 450 < range <= 500:
                Attack_Rating = 6
            elif 500 < range <= 750:
                Attack_Rating = 5
            elif 750 < range <= 1000:
                Attack_Rating = 3
            elif 1000 < range <= 1500:
                Attack_Rating = 1
            else:
                Attack_Rating = 0
        if firing_unit == "BMP_gun" and target_unit == "APC":
            if range <= 300:
                Attack_Rating = 8
            elif 300 < range <= 450:
                Attack_Rating = 7
            elif 450 < range <= 500:
                Attack_Rating = 6
            elif 500 < range <= 750:
                Attack_Rating = 5
            elif 750 < range <= 1000:
                Attack_Rating = 3
            elif 1000 < range <= 1500:
                Attack_Rating = 2
            else:
                Attack_Rating = 0
        if firing_unit == "Sagger" and target_unit == "Tank" or target_unit =="APC":
            if range <= 400:
                Attack_Rating = 0
            elif 400 < range <= 450:
                Attack_Rating = 6
            elif 450 < range <= 750:
                Attack_Rating = 7
            elif 750 < range <= 3000:
                Attack_Rating = 9
            else:
                Attack_Rating = 0
        if firing_unit == "XMBT" and target_unit == "Tank":
            if range <= 1500:
                Attack_Rating = 10
            elif 1500 < range <= 2000:
                Attack_Rating = 9
            elif 2000 < range <= 3000:
                Attack_Rating = 8
            else:
                Attack_Rating = 0
        if firing_unit == "XMBT" and target_unit == "APC":
            if range <= 1500:
                Attack_Rating = 10
            elif 1500 < range <= 2000:
                Attack_Rating = 9
            elif 2000 < range <= 2500:
                Attack_Rating = 8
            elif 2500 < range <= 3000:
                Attack_Rating = 5
            else:
                Attack_Rating = 0

        if target_unit == "Tank" or target_unit =="APC": # 归类
            target_unit = "vehicle_combatant"

        # ----苏军火力单位对苏军人员攻击效果评价表：combat result table,CRT
        if target_unit == "soveit_combatant":
            if firing_unit == "TM+":
                if range <= 50:
                    Attack_Rating = 9
                elif 50 < range <= 200:
                    Attack_Rating = 8
                elif 200 < range <= 350:
                    Attack_Rating = 7
                elif 350 < range <= 400:
                    Attack_Rating = 6
                elif 400 < range <= 450:
                    Attack_Rating = 5
                elif 450 < range <= 500:
                    Attack_Rating = 4
                elif 500 < range <= 750:
                    Attack_Rating = 2
                elif 750 < range <= 1000:
                    Attack_Rating = 1
                else:
                    Attack_Rating = 0
            if firing_unit == "TM":
                if range <= 50:
                    Attack_Rating = 8
                elif 50 < range <= 200:
                    Attack_Rating = 7
                elif 200 < range <= 350:
                    Attack_Rating = 6
                elif 350 < range <= 400:
                    Attack_Rating = 5
                elif 400 < range <= 450:
                    Attack_Rating = 4
                elif 450 < range <= 500:
                    Attack_Rating = 2
                else:
                    Attack_Rating = 0
            if firing_unit == "MG":
                if range <= 500:
                    Attack_Rating = 3
                elif 500 < range <= 750:
                    Attack_Rating = 2
                elif 750 < range <= 1000:
                    Attack_Rating = 1
                else:
                    Attack_Rating = 0
            if firing_unit == "MG+":
                if range <= 500:
                    Attack_Rating = 4
                elif 500 < range <= 1000:
                    Attack_Rating = 3
                elif 1000 < range <= 2000:
                    Attack_Rating = 2
                else:
                    Attack_Rating = 0
            if firing_unit == "BMP":
                if range <= 50:
                    Attack_Rating = 6
                elif 50 < range <= 500:
                    Attack_Rating = 7
                elif 500 < range <= 1000:
                    Attack_Rating = 4
                elif 1000 < range <= 1500:
                    Attack_Rating = 2
                elif 1500 < range <= 2000:
                    Attack_Rating = 1
                else:
                    Attack_Rating = 0
            if firing_unit == "T62":
                if range <= 50:
                    Attack_Rating = 4
                elif 50 < range <= 500:
                    Attack_Rating = 5
                elif 500 < range <= 1000:
                    Attack_Rating = 4
                elif 1000 < range <= 1500:
                    Attack_Rating = 3
                elif 1500 < range <= 2500:
                    Attack_Rating = 2
                else:
                    Attack_Rating = 0
            if firing_unit == "XMBT":
                if range <= 1500:
                    Attack_Rating = 6
                elif 1500 < range <= 2500:
                    Attack_Rating = 5
                elif 2500 < range <= 3000:
                    Attack_Rating = 3
                else:
                    Attack_Rating = 0

        goal_piece.direct_rating = Attack_Rating

        # ---------反车辆战斗结果表----------------------------------------
        if target_unit == "vehicle_combatant":  # 攻击车辆时
            if Dice_roll == 2:
                if 1 <= Attack_Rating <= 8:
                    result = "kf"
                if 9 <= Attack_Rating <= 11:
                    result = "k"
            if Dice_roll == 3:
                if 1 <= Attack_Rating <= 2:
                    result = "no_effect"
                if 3 <= Attack_Rating <= 11:
                    result = "k"
            if Dice_roll == 4:
                if 1 <= Attack_Rating <= 4:
                    result = "no_effect"
                if 5 <= Attack_Rating <= 11:
                    result = "k"
            if Dice_roll == 5:
                if 1 <= Attack_Rating <= 6:
                    result = "no_effect"
                if 7 <= Attack_Rating <= 11:
                    result = "k"
            if Dice_roll == 6:
                if 1 <= Attack_Rating <= 8:
                    result = "no_effect"
                if 9 <= Attack_Rating <= 11:
                    result = "k"
            if Dice_roll == 7:
                if 1 <= Attack_Rating <= 10:
                    result = "no_effect"
                if Attack_Rating == 11:
                    result = "k"
            if Dice_roll == 8:
                if 1 <= Attack_Rating <= 9:
                    result = "no_effect"
                if 10 <= Attack_Rating <= 11:
                    result = "k"
            if Dice_roll == 9:
                if 1 <= Attack_Rating <= 7:
                    result = "no_effect"
                if 8 <= Attack_Rating <= 11:
                    result = "k"
            if Dice_roll == 10:
                if 1 <= Attack_Rating <= 5:
                    result = "no_effect"
                if 6 <= Attack_Rating <= 11:
                    result = "k"
            if Dice_roll == 11:
                if 1 <= Attack_Rating <= 3:
                    result = "no_effect"
                if 4 <= Attack_Rating <= 11:
                    result = "k"
            if Dice_roll == 12:
                if Attack_Rating == 1:
                    result = "no_effect"
                if 4 <= Attack_Rating <= 11:
                    result = "km"
            # ------特殊地形情况----------
            if landform == " 城  镇":
                if Dice_roll == 2:
                    result = "no_effect"
            if landform == " 森  林":
                if Dice_roll == 3 or 4:
                    result = "no_effect"
            if spe_event == 1:
                if Dice_roll >= 5:
                    result = "no_effect"
            if spe_event == 2:
                if Dice_roll >= 7:
                    result = "no_effect"

        if target_unit == "soveit_combatant":  # 攻击人员时
            if Dice_roll == 2:
                if 1 <= Attack_Rating <= 3:
                    result = "s"
                if 4 <= Attack_Rating <= 9:
                    result = "k"
            if Dice_roll == 3:
                if 1 <= Attack_Rating <= 1:
                    result = "no_effect"
                if 2 <= Attack_Rating <= 4:
                    result = "s"
                if 5 <= Attack_Rating <= 9:
                    result = "k"
            if Dice_roll == 4:
                if 1 <= Attack_Rating <= 3:
                    result = "no_effect"
                if 4 <= Attack_Rating <= 7:
                    result = "s"
                if 8 <= Attack_Rating <= 9:
                    result = "k"
            if Dice_roll == 5:
                if 1 <= Attack_Rating <= 4:
                    result = "no_effect"
                if 5 <= Attack_Rating <= 9:
                    result = "s"
            if Dice_roll == 6:
                if 1 <= Attack_Rating <= 5:
                    result = "no_effect"
                if 6 <= Attack_Rating <= 9:
                    result = "s"
            if Dice_roll == 7:
                if 1 <= Attack_Rating <= 6:
                    result = "no_effect"
                if 7 <= Attack_Rating <= 9:
                    result = "s"
            if Dice_roll == 8:
                if 1 <= Attack_Rating <= 6:
                    result = "no_effect"
                if 7 <= Attack_Rating <= 9:
                    result = "s"
            if Dice_roll == 9:
                if 1 <= Attack_Rating <= 5:
                    result = "no_effect"
                if 6 <= Attack_Rating <= 9:
                    result = "s"
            if Dice_roll == 10:
                if 1 <= Attack_Rating <= 4:
                    result = "no_effect"
                if 5 <= Attack_Rating <= 8:
                    result = "s"
                if Attack_Rating == 9:
                    result = "k"
            if Dice_roll == 11:
                if 1 <= Attack_Rating <= 2:
                    result = "no_effect"
                if 3 <= Attack_Rating <= 7:
                    result = "s"
                if 8 <= Attack_Rating <= 9:
                    result = "k"
            if Dice_roll == 12:
                if 1 <= Attack_Rating <= 6:
                    result = "s"
                if 7 <= Attack_Rating <= 9:
                    result = "k"

            # ---------特殊地形情况---------
            if landform == " 城  镇" or landform == " 城  镇"" 森  林":
                if Dice_roll <= 4:
                    result = "no_effect"
            if landform == " 遮  障":
                if Dice_roll >= 7:
                    result = "no_effect"
        return result

    def direct_shoot(self, shot_piece, goal_piece, shot_hex, goal_hex):  # 直瞄火力裁决
        dis = self.distanse(shot_hex, goal_hex) # 距离得出
        goal_piece.direct_dis = dis
        Dice_roll1 = random.randint(1, 6)
        Dice_roll2 = random.randint(1, 6)
        Dice_roll = Dice_roll1 + Dice_roll2  # 用于生成指定范围内的整数的随机数
        goal_piece.Dice = Dice_roll
        goal_piece.goal_piece = True # 被选作目标棋子
        landform = goal_hex.landform
        firing_unit = ""
        target_unit = ""
        result = ""
        if shot_piece.piece_name[:3] == "red":
            firing_unit = shot_piece.piece_name[4:]
            if goal_piece.piece_name[5:] == "M60A1": # 待扩充
                target_unit = "Tank"
            result = self.Effectiveness_redtoblue(firing_unit, target_unit, dis, landform, Dice_roll, goal_piece)

        else:
            firing_unit = shot_piece.piece_name[5:]
            if goal_piece.piece_name[4:] == "T62":
                target_unit = "Tank"
            result = self.Effectiveness_bluetored(firing_unit, target_unit, dis, landform, Dice_roll, goal_piece)

        return result


    def hex_pick(self, hex, last_pos):  # 机动阶段对六角格的点选，只能选择相邻六角格
        self.dis_max = 67
        self.dis_min = 60
        self.hex = hex
        self.cost = 1  # 暂不考虑地形，视所有地形的机动力消耗均为1
        #-----区分地形(ID:编号，elevation：高度，landform：地形----

        if self.last_hex.landform == ' 道  路' and self.hex.landform == ' 道  路':
            self.cost = 0.5
        if self.hex.landform == ' 城  镇' or self.hex.landform == ' 森  林' or self.hex.landform == ' 河  流':
            self.cost = 2

        self.last_pos = last_pos
        self.dis = (hex.pos_hex_rect.centerx - last_pos[0]) ** 2 + (hex.pos_hex_rect.centery - last_pos[1]) ** 2  # 距离的平方
        if self.dis_min ** 2 < self.dis and self.dis < self.dis_max ** 2 and self.piece_move_point >= self.cost:
            hex.active = True
            self.click_pos = self.hex.pos_hex_rect.center
            self.piece_move_point -= self.cost
            self.last_hex = hex
            self.hex_list.append(hex) # 进队列
            self.line_list.append(hex.pos_hex_rect.center) # 路线的点


    # 鼠标点选操作
    def mouse_pick(self):
        # 绑定鼠标精灵mouse_sprite,用于选取对象，进行碰撞检测
        if self.Mouse_left_down and not self.Mouse_right_down and self.Mouse_drag_measure != 1:
            # 拖放时把鼠标变为手形，并把位置放于形状中心位置
            pg.mouse.set_visible(False)
            self.image = pg.image.load('mouse_icon/mouse_drag.png').convert_alpha()#鼠标图案变成抓取样
            self.rect.center = pg.mouse.get_pos() #鼠标图案移动
            self.screen.blit(self.image, self.rect)

            if self.GUI_state == 2 or (self.GUI_state == 6 and self.indirect_state == 0): # 部署阶段与间瞄裁决的第一个小阶段
                for pieces_list in self.red_pieces:
                    if pieces_list.active == 1:
                        pieces_list.pos_piece_rect.center = pg.mouse.get_pos()  # 棋子随鼠标移动
                        pg.time.delay(20)
                # ----激活棋子，棋子随鼠标而动-----
                for pieces_list in self.blue_pieces:  # 遍历蓝方棋子
                    if pieces_list.active == 1:
                        pieces_list.pos_piece_rect.center = pg.mouse.get_pos()  # 棋子随鼠标移动
                        pg.time.delay(20)

            else:
                pass  # 待扩充


        elif self.Mouse_right_down and self.Mouse_left_down and self.Mouse_drag_measure == 1:
            pg.mouse.set_visible(False)
            self.image = pg.image.load('mouse_icon/aim_cross.png').convert_alpha()
            self.rect.center = pg.mouse.get_pos()
            self.screen.blit(self.image, self.rect)
        else:
            pg.mouse.set_visible(False)
            self.image = pg.image.load('mouse_icon/mouse_click.png').convert_alpha()
            self.rect.center = pg.mouse.get_pos()
            self.screen.blit(self.image, self.rect)
        if self.Mouse_right_down is True and not self.Mouse_left_down:
            # -------拖放时把鼠标变为手形，并把位置放于形状中心位置--------------------------------
            pg.mouse.set_visible(False)
            self.image = pg.image.load('mouse_icon/mouse_drag.png').convert_alpha()
            self.rect.center = pg.mouse.get_pos()
            self.screen.blit(self.image, self.rect)
            '''
            # -------释放选取红方的棋子-----------------
            for pieces_list in self.red_pieces:
                if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()):
                    pieces_list.pos_piece_rect.center = pg.mouse.get_pos()  # 棋子随鼠标移动
                    pieces_list.status = 0  # 释放棋子
            # -------选取蓝方的棋子-----------------
            for pieces_list in self.blue_pieces:  # 判断鼠标是否在蓝方矩形区内
                if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()):
                    pieces_list.pos_piece_rect.center = pg.mouse.get_pos()  # 棋子随鼠标移动
                    pieces_list.status = 0  # 释放棋子
            '''
        elif not self.Mouse_left_down:
            pg.mouse.set_visible(False)
            self.image = pg.image.load('mouse_icon/mouse_click.png').convert_alpha()
            self.rect.center = pg.mouse.get_pos()
            self.screen.blit(self.image, self.rect)

        if self.Mouse_left_click is True:
            if self.GUI_state == 4: # 机动阶段
                if self.Red_move is True:
                    for pieces_list in self.red_pieces:  # 机动阶段棋子的点选
                        if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()) and pieces_list.move_ability is True:  # 标记棋子，使其变为活跃态
                            while len(self.line_list): # 清除路线
                                self.line_list.pop(0)
                            self.line_list.append(pieces_list.pos_piece_rect.center)
                            for hex_list in self.hex_group:  # 重选棋子后六角格均重置为非激活状态
                                hex_list.active = False
                                if hex_list.pos_hex_rect.collidepoint(pieces_list.pos_piece_rect.center): # 确定棋子所在六角格位置
                                    self.last_hex = hex_list
                            self.last_piece.status_move = False
                            pieces_list.status_move = True  # 机动阶段被激活状态
                            self.last_piece = pieces_list
                            self.piece_move_point = pieces_list.move_point  # 将棋子的机动值赋予给辅助变量
                            self.click_pos = pieces_list.pos_piece_rect.center  # 将所选中棋子的中心记录下来
                            break

                if not self.Red_move:
                    for pieces_list in self.blue_pieces:  # 遍历蓝方棋子
                        if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()) and pieces_list.move_ability is True:  # 标记棋子，使其变为活跃态
                            while len(self.line_list):
                                self.line_list.pop(0)
                            self.line_list.append(pieces_list.pos_piece_rect.center)
                            for hex_list in self.hex_group:  # 重选棋子后六角格均重置为非激活状态
                                hex_list.active = False
                                if hex_list.pos_hex_rect.collidepoint(pieces_list.pos_piece_rect.center): # 确定棋子所在六角格位置
                                    self.last_hex = hex_list
                            self.last_piece.status_move = False
                            pieces_list.status_move = True  # 机动阶段被激活状态
                            self.last_piece = pieces_list
                            self.piece_move_point = pieces_list.move_point  # 将棋子的机动值赋予给辅助变量
                            self.click_pos = pieces_list.pos_piece_rect.center  # 将所选中棋子的中心记录下来
                            break

                if self.last_hex.pos_hex_rect.collidepoint(pg.mouse.get_pos()) and len(self.hex_list):  # 机动触发条件：如果点击上一个选中的六角格
                    while len(self.hex_list):
                        Hex = self.hex_list.pop(0)
                        self.last_piece.pos_piece_rect.center = Hex.pos_hex_rect.center  # 机动
                    self.last_piece.move_ability = False  # 机动完毕，该棋子失去机动力
                    self.last_piece.FIRE = False # 机动后的棋子失去射击能力


                for hex_list in self.hex_group:
                    if hex_list.pos_hex_rect.collidepoint(pg.mouse.get_pos()) and not hex_list.pos_hex_rect.collidepoint(self.last_piece.pos_piece_rect.center):
                        self.hex_pick(hex_list, self.click_pos)
                        pg.time.delay(20)


                '''
                # 改用完美碰撞检测
                hex_choose = pg.sprite.spritecollide(self, self.hex_group, True, pg.sprite.collide_mask)
                if hex_choose:
                    for hex_list in hex_choose:
                        if not hex_list.pos_hex_rect.collidepoint(self.last_piece.pos_piece_rect.center):
                            self.hex_pick(hex_list, self.click_pos)
                '''

            elif self.GUI_state == 3: # 直瞄射击
                if self.Red_shot is True:
                    for pieces_list in self.red_pieces:
                        if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()) and pieces_list.FIRE is True: # 标记棋子，使其变为活跃态
                            self.shot_piece.status_shot = False # 上一个棋子变成非射击棋子
                            self.shot_piece.fire_prepare = False # 移除射击准备状态
                            self.shot_piece = pieces_list # 射击棋子
                            self.shot_piece.status_shot = True # 新选中的棋子变成射击棋子
                            self.goal_piece.goal_piece = False # 目标棋子更新
                            for hex_list in self.hex_group:
                                if hex_list.pos_hex_rect.collidepoint(pg.mouse.get_pos()):
                                    self.shot_hex = hex_list # 获取射击棋子所在六角格，便于计算距离

                    if self.shot_piece.fire_prepare == True:
                        for pieces_list in self.blue_pieces:
                            if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()):
                                self.goal_piece = pieces_list
                                for hex_list in self.hex_group:
                                    if hex_list.pos_hex_rect.collidepoint(pg.mouse.get_pos()):
                                        self.goal_hex = hex_list  # 获取目标棋子所在六角格，便于计算距离
                                self.shoot_result = self.direct_shoot(self.shot_piece, self.goal_piece, self.shot_hex, self.goal_hex)
                                self.shoot_result = "k" # 测试用
                                if self.shoot_result == "k": # 歼灭
                                    self.goal_piece.status = 5
                                elif self.shoot_result == "s": # 压制
                                    self.goal_piece.status = 2
                                elif self.shoot_result == "km": # 丧失机动
                                    if self.goal_piece.status != 3:
                                        self.goal_piece.status = 3
                                    else:
                                        self.shoot_result = "k"
                                elif self.shoot_result == "kf": # 丧失火力
                                    if self.goal_piece.status != 4:
                                        self.goal_piece.status = 4
                                    else:
                                        self.shoot_result = "k"
                                elif self.shoot_result == "no_effect": # 无效
                                    self.goal_piece.status = 7
                                print(self.shoot_result)
                                # self.screen.blit(self.goal_piece.Hit_images[3],pieces_list.pos_piece_rect.center)
                                self.shoot_sound.play()
                                self.shot_piece.FIRE = False
                                self.shot_piece.fire_prepare = False # 防止多次射击
                                self.shot_piece.move_ability = 0 # 射击后失去机动力

                elif not self.Red_shot:
                    for pieces_list in self.blue_pieces:
                        if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()) and pieces_list.FIRE is True: # 标记棋子，使其变为活跃态
                            self.shot_piece.status_shot = False # 上一个棋子变成非射击棋子
                            self.shot_piece.fire_prepare = False # 移除射击准备状态
                            self.shot_piece = pieces_list # 射击棋子
                            self.shot_piece.status_shot = True # 新选中的棋子变成射击棋子
                            self.goal_piece.goal_piece = False # 目标棋子更新
                            for hex_list in self.hex_group:
                                if hex_list.pos_hex_rect.collidepoint(pg.mouse.get_pos()):
                                    self.shot_hex = hex_list # 获取射击棋子所在六角格，便于计算距离

                    if self.shot_piece.fire_prepare == True:
                        for pieces_list in self.red_pieces:
                            if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()):
                                self.goal_piece = pieces_list
                                for hex_list in self.hex_group:
                                    if hex_list.pos_hex_rect.collidepoint(pg.mouse.get_pos()):
                                        self.goal_hex = hex_list  # 获取目标棋子所在六角格，便于计算距离
                                self.shoot_result = self.direct_shoot(self.shot_piece, self.goal_piece, self.shot_hex, self.goal_hex)
                                # self.shoot_result = "km" # 测试用
                                if self.shoot_result == "k": # 歼灭
                                    self.goal_piece.status = 5
                                elif self.shoot_result == "s": # 压制
                                    self.goal_piece.status = 2
                                elif self.shoot_result == "km":  # 丧失机动
                                    if self.goal_piece.status != 3:
                                        self.goal_piece.status = 3
                                    else:
                                        self.shoot_result = "k"
                                elif self.shoot_result == "kf":  # 丧失火力
                                    if self.goal_piece.status != 4:
                                        self.goal_piece.status = 4
                                elif self.shoot_result == "no_effect": # 无效
                                    self.goal_piece.status = 7
                                print(self.shoot_result)
                                self.shoot_sound.play()
                                # self.screen.blit(self.goal_piece.Hit_images[3], pieces_list.pos_piece_rect.center)
                                #------播放射击动画-------
                                # Show_Text = wel_font.render("击毁", True, RED_COLOUR, BLACK_COLOUR)
                                #screen = pg.display.get_surface()
                                #screen.blit(Show_Text, pieces_list.pos_piece_rect.center)
                                    # self.goal_piece.destroy()
                                self.shot_piece.FIRE = False
                                self.shot_piece.fire_prepare = False # 防止多次射击
                                self.shot_piece.move_ability = 0 # 射击后失去机动力


        if self.Mouse_right_click is True:
            if self.GUI_state == 3:
                if self.shot_piece.FIRE is True:
                    self.shot_piece.fire_prepare = True



    # 鼠标事件处理
    def mouse_event_handling(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: #关闭
                pg.quit()
                sys.exit()
            elif event.type == MOUSEMOTION: #鼠标移动
                pos_mouse_pos = pg.mouse.get_pos()
                #self.screen.blit(BASICFONT.render('mouse location:' + str(pos_mouse_pos),
                                                  # True, (0, 255, 0)), (200, 560)) # 显示鼠标位置，测试用
            elif event.type == MOUSEBUTTONDOWN: #鼠标按下事件
                self.pos_click = pg.mouse.get_pos()
                pressed_array = pg.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:  # 鼠标左键点击
                            pass
                        elif index == 1:
                            pass
                        elif index == 2:
                            pass
                if event.button == 1:
                    self.Mouse_left_down = True
                    if self.GUI_state == 2: # 部署
                        for pieces_list in self.red_pieces:  # 红方棋子选中
                            if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()):
                                # pieces_list.status = not pieces_list.status  # 激活变为非激活，非激活变为激活
                                pieces_list.active = 1  # 选中棋子,活动，显示边框
                                self.piece_choise = True  # 表明已有红方棋子被选中了，不用经历蓝方棋子的循环，以免覆盖
                                break  # 作用是只允许选取一个棋子，但可能不是最上层的棋子-----待改进
                        if not self.piece_choise:
                            for pieces_list in self.blue_pieces:  # 蓝方棋子选中
                                if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()):
                                    # pieces_list.status = not pieces_list.status
                                    pieces_list.active = 1  # 选中棋子,活动，显示边框
                                    break
                        self.piece_choise = False  # 重置

                    elif self.GUI_state == 6: # 间瞄阶段
                        for pieces_list in self.red_pieces:  # 红方棋子选中
                            if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()):
                                if pieces_list.piece_name == "red_120mm" or pieces_list.piece_name == "red_122mm" or pieces_list.piece_name == "red_152mm":
                                    # pieces_list.status = not pieces_list.status  # 激活变为非激活，非激活变为激活
                                    pieces_list.active = 1  # 选中棋子,活动，显示边框
                                    self.piece_choise = True  # 表明已有红方棋子被选中了，不用经历蓝方棋子的循环，以免覆盖
                                    break  # 作用是只允许选取一个棋子，但可能不是最上层的棋子-----待改进

                        if not self.piece_choise:
                            for pieces_list in self.blue_pieces:  # 蓝方棋子选中
                                if pieces_list.pos_piece_rect.collidepoint(pg.mouse.get_pos()):
                                    if pieces_list.piece_name == "blue_4.2''" or pieces_list.piece_name == "blue_81mm" :
                                        # pieces_list.status = not pieces_list.status
                                        pieces_list.active = 1  # 选中棋子,活动，显示边框
                                        break

                        self.piece_choise = False  # 重置

                    # if maneuver_rect.collidepoint(pg.mouse.get_pos()):
                    #     MANEUVER_MOVEABLE += 1
                    #     if MANEUVER_MOVEABLE == 1:
                    #         print('开始机动，请右击选择路径！')
                    #     elif MANEUVER_MOVEABLE == 2:
                    #         print('机动结束！')
                    # if indirectshot_rect.collidepoint(pg.mouse.get_pos()):
                    #     hldd = True
                    # --ZHQ--
                    Game_Turn = True  # 开始推演
                elif event.button == 2:
                    self.Mouse_mid_click = True
                    self.scenario.terrain.map_scale_ratio = 1.0 #恢复原来状态
                elif event.button == 3:
                    self.Mouse_right_down = True
                elif event.button == 4:  # 中键向前
                    self.Mouse_mid_forward = True
                    if self.scenario.terrain.map_scale_ratio < 5:
                        self.scenario.terrain.map_scale_ratio += 0.1
                elif event.button == 5:  # 中键向后
                    self.Mouse_mid_backward = True
                    if self.scenario.terrain.map_scale_ratio > 0.3:
                        self.scenario.terrain.map_scale_ratio -= 0.1

            elif event.type == MOUSEBUTTONUP: #鼠标释放
                if event.button == 1: #鼠标左键释放时，所有棋子均变为非激活状态
                    self.Mouse_left_down = False
                    self.Mouse_left_click = True
                    if self.GUI_state == 2 or (self.GUI_state == 6 and self.indirect_state == 0): # 为了避免与其他阶段的点选冲突，以下动作归为部署阶段
                        # ----------选中六角格-----------
                        for hex_list in self.hex_group:
                            if hex_list.pos_hex_rect.collidepoint(pg.mouse.get_pos()):
                                break  # 选中这个六角格
                        # ----------释放红方棋子------------
                        for pieces_list in self.red_pieces:
                            if pieces_list.active == 1:
                                # ------将棋子中心粘滞于六角格中心------
                                pieces_list.pos_piece_rect.center = [hex_list.pos_hex_rect.centerx, hex_list.pos_hex_rect.centery]
                                pieces_list.active = 0  # 变为非激活状态
                                break
                        for pieces_list in self.blue_pieces:
                            if pieces_list.active == 1:
                                # ------将棋子中心粘滞于六角格中心------
                                pieces_list.pos_piece_rect.center = [hex_list.pos_hex_rect.centerx, hex_list.pos_hex_rect.centery]
                                pieces_list.active = 0  # 变为非激活状态
                                break

                elif event.button == 3:
                    self.Mouse_right_down = False
                    self.Mouse_right_click = True
            elif event.type == VIDEORESIZE:
                bg_size = event.size
                width, height = bg_size
                main_screen_fight = pg.display.set_mode(bg_size, RESIZABLE, 32)
            elif event.type == USEREVENT:
                # print("计划火力时间到！！！")
                pg.time.set_timer(FIREPLOT_TIME, 0)
                # time_sound.stop()