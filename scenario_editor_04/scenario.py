import pygame as pg

from pieces_manager_02.piece import BTank, RTank, RPlane, BVehicle, RVehicle, BPlane
from resources.load_data import GRAPHICS


class Scenario_1(object):
    '''
    通过硬代码的方式将算子位置呈现在地图上
    存在算子堆叠问题，目前暂未想好合适的编号方法
    '''
    # 设置无人机数量，1代表想定有无人机，可选0-4个无人机
    # UAV_list = [1, 1, 1, 1]
    UAV_list = [1, 1, 1, 1]

    def __init__(self, wargame=None, name=None, index=None, terrain=None):
        self.wargame_env = wargame
        self.blue_pieces = pg.sprite.Group()
        self.red_pieces = pg.sprite.Group()
        self.name = name  # 想定名称
        self.index = index  # 想定编号
        self.terrain = terrain  # 想定地形
        self.blue_tank_1 = BTank(self.wargame_env, 15, 40, self.blue_pieces)
        self.blue_tank_2 = BTank(self.wargame_env, 16, 41, self.blue_pieces)
        self.blue_tank_3 = BTank(self.wargame_env, 17, 41, self.blue_pieces)
        self.blue_tank_4 = BTank(self.wargame_env, 18, 40, self.blue_pieces)
        self.blue_tank_5 = BTank(self.wargame_env, 18, 41, self.blue_pieces)
        self.blue_tank_6 = BTank(self.wargame_env, 17, 40, self.blue_pieces)
        self.blue_tank_7 = BTank(self.wargame_env, 16, 40, self.blue_pieces)
        self.blue_tank_8 = BTank(self.wargame_env, 15, 41, self.blue_pieces)
        self.blue_tank_9 = BTank(self.wargame_env, 18, 42, self.blue_pieces)
        self.blue_tank_10 = BTank(self.wargame_env, 17, 42, self.blue_pieces)
        self.blue_action_history = []
        self.blue_operation_hex = []
        # 40.8

        self.red_tank_1 = RTank(self.wargame_env, 17, 7, self.red_pieces)
        self.red_tank_2 = RTank(self.wargame_env, 18, 8, self.red_pieces)
        self.red_tank_3 = RTank(self.wargame_env, 19, 8, self.red_pieces)
        self.red_tank_4 = RTank(self.wargame_env, 16, 8, self.red_pieces)
        self.red_tank_5 = RTank(self.wargame_env, 17, 8, self.red_pieces)
        self.red_tank_6 = RTank(self.wargame_env, 17, 6, self.red_pieces)
        self.red_tank_7 = RTank(self.wargame_env, 16, 7, self.red_pieces)
        self.red_tank_8 = RTank(self.wargame_env, 18, 9, self.red_pieces)
        # 6.625

        if self.UAV_list[0] == 1:
            self.red_plane_9 = RPlane(self.wargame_env, 16, 4, self.red_pieces)
        else:
            pass

        if self.UAV_list[1] == 1:
            self.red_plane_10 = RPlane(self.wargame_env, 17, 4, self.red_pieces)
        else:
            pass

        if self.UAV_list[2] == 1:
            self.red_plane_11 = RPlane(self.wargame_env, 18, 4, self.red_pieces)
        else:
            pass

        if self.UAV_list[3] == 1:
            self.red_plane_12 = RPlane(self.wargame_env, 19, 4, self.red_pieces)
        else:
            pass

        self.red_action_history = []
        self.red_operation_hex = []

        # 设置夺控点坐标
        self.goal = (14, 24)
        self.goal_sprite = pg.sprite.Sprite(self.red_pieces)
        self.goal_sprite.image = pg.transform.scale(GRAPHICS['Control points'], (50, 50))
        self.goal_sprite.rect = pg.Rect(0, 0, 50, 50)
        self.state_controlpoint = None  # 判断夺控要点被哪方夺占:red_control/blue_control

    def goal_update(self, dt):
        offset = self.wargame_env.game_map.map_offset
        self.goal_sprite.rect.center = (self.goal[1] * 54 + 27 + 5 - offset[0], self.goal[0] * 45 + 60 / 2 + 4 - offset[1])

    def update(self, dt):
        if self.blue_tank_1.num <= 0:
            self.blue_tank_1.kill()
        if self.blue_tank_2.num <= 0:
            self.blue_tank_2.kill()
        if self.blue_tank_3.num <= 0:
            self.blue_tank_3.kill()
        if self.blue_tank_4.num <= 0:
            self.blue_tank_4.kill()
        if self.blue_tank_5.num <= 0:
            self.blue_tank_5.kill()
        if self.blue_tank_6.num <= 0:
            self.blue_tank_6.kill()
        if self.blue_tank_7.num <= 0:
            self.blue_tank_7.kill()
        if self.blue_tank_8.num <= 0:
            self.blue_tank_8.kill()
        if self.blue_tank_9.num <= 0:
            self.blue_tank_9.kill()
        if self.blue_tank_10.num <= 0:
            self.blue_tank_10.kill()

        if self.red_tank_1.num <= 0:
            self.red_tank_1.kill()
        if self.red_tank_2.num <= 0:
            self.red_tank_2.kill()
        if self.red_tank_3.num <= 0:
            self.red_tank_3.kill()
        if self.red_tank_4.num <= 0:
            self.red_tank_4.kill()
        if self.red_tank_5.num <= 0:
            self.red_tank_5.kill()
        if self.red_tank_6.num <= 0:
            self.red_tank_6.kill()
        if self.red_tank_7.num <= 0:
            self.red_tank_7.kill()
        if self.red_tank_8.num <= 0:
            self.red_tank_8.kill()

        if self.UAV_list[0] == 1:
            if self.red_plane_9.num <= 0:
                self.red_plane_9.kill()
        else:
            pass

        if self.UAV_list[1] == 1:
            if self.red_plane_10.num <= 0:
                self.red_plane_10.kill()
        else:
            pass

        if self.UAV_list[2] == 1:
            if self.red_plane_11.num <= 0:
                self.red_plane_11.kill()
        else:
            pass

        if self.UAV_list[3] == 1:
            if self.red_plane_12.num <= 0:
                self.red_plane_12.kill()
        else:
            pass

        self.blue_pieces.update(dt)
        self.red_pieces.update(dt)
        # 夺控点更新
        self.goal_update(dt)

    def draw(self, surface):
        self.blue_pieces.draw(surface)
        self.red_pieces.draw(surface)

#
# class Player(object):
#     '''
#     设置红蓝双方对阵员，目前可用鼠标控制算子状态切换，进行动作
#     '''
#
#     def __init__(self, wargame, player, piece):
#         self.wargame_env = wargame
#         self.player = player
#         self.piece = piece
#
#     def get_event(self, event):
#         if event.type == pg.MOUSEBUTTONDOWN:
#             mouse_pos = pg.mouse.get_pos()
#             if event.button == 1:  # 左键单击
#                 x, y = self.wargame_env.game_map.mouse_pos_to_map_id(mouse_pos)
#                 if self.piece.state == '机动':
#                     self.piece_move(x, y)
#                 elif self.piece.state == '行军':
#                     self.piece_march(x, y)
#                 elif self.piece.state == '直瞄射击':
#                     self.piece_fire(x, y)
#                 elif self.piece.state == '间瞄射击':
#                     self.indirect_fire(x, y)
#
#     @property
#     def score(self):
#         return self.piece.score
#
#     def do_action(self):
#         pass
#
#     def get_piece_state(self, piece):
#         return piece.get_state()
#
#     def piece_move(self, x, y):
#         if (x, y) in self.wargame_env.game_map.get_neighbour(self.piece.co_x, self.piece.co_y):
#             self.piece.move_one_step(x, y)
#
#     def piece_march(self, x, y):
#         if (x, y) in self.wargame_env.game_map.get_neighbour(self.piece.co_x, self.piece.co_y):
#             self.piece.march_one_step(x, y)
#
#     def piece_fire(self, x, y):
#         if self.player == 'red':
#             if self.wargame_env.blue_player.piece.co_x == x and self.wargame_env.blue_player.piece.co_y == y:
#                 self.piece.fire(self.wargame_env.blue_player.piece)
#         elif self.player == 'blue':
#             if self.wargame_env.red_player.piece.co_x == x and self.wargame_env.red_player.piece.co_y == y:
#                 self.piece.fire(self.wargame_env.red_player.piece)
#
#     def piece_hide(self):
#         self.piece.hide()
#
#     def indirect_fire(self, x, y):
#         self.piece.fire(x, y)
#
#     def update(self, dt):
#         self.piece.update(dt)
#
#     def refresh(self):
#         self.piece.refresh()

# class Scenario(object):
#     def __init__(self, name, index, terrain):  # 用包裹关键字传递:pieces是一个字典，收集所有的关键字。在不明确需要多少变量时用
#         self.name = name  # 想定名称
#         self.index = index  # 想定编号
#         self.terrain = terrain
#         self.bg_image = terrain.image
#         self.red_pieces = pg.sprite.Group()  # 红方任务编成
#         self.blue_pieces = pg.sprite.Group()  # 蓝方任务编成
#         self.pieces = {}  # 想定中的算子类型,字典:{"red_T62":Pieces("red_T62"),"blue_M60A1:Piece("blue_M60A1")}
#         self.piece_group = pg.sprite.Group()  # 算子总库：红方+蓝方算子
#         self.init_pos = {}  # 想定中双方力量的初始部署位置
#
#         # 把传递进来的字典变量：pieces_group，赋值给内部字典变量self.pieces
#         # for piece_name in pieces_group:
#         #     self.pieces[piece_name] = pieces_group[piece_name]
#         # 想定交互式对话框定义
#
#     # 加载任务编成
#     def load_task_organization(self, piece_name, piece_num):
#         if piece_name[:3] == "red":  # 加入到红方
#             for i in range(piece_num):
#                 self.red_pieces.add(Piece(piece_name))
#         elif piece_name[:4] == "blue":
#             for i in range(piece_num):  # 加入到蓝方
#                 self.blue_pieces.add(Piece(piece_name))
#
#     # 红方算子名称：red_T62、red_BMP、red_BRDM、red_TM、red_GUN
#     # 蓝方算子名称：blue_M60A1、blue_M113、blue_M150、blue_TM、blue_GUN
#     # 标记名称：impact_marker、smoker_marker、wreck_marker、mine_marker、suppression_marker、kill_firepower_marker、kill_mobility_marker
#
#     # 初始化部署位置
#     def init_deployment(self, piece_name, ini_position=NONE):
#         red_i = 0
#         blue_j = 0
#         if self.terrain.name == "mapA":
#             if piece_name[:3] == "red":
#                 for red_list in self.red_pieces:
#                     if ini_position[red_i][0] % 2 == 1:
#                         red_list.pre_piece_rect.topleft = (
#                         5 + 113 * (ini_position[red_i][0] - 1) / 2, 7.5 + 63.3 * (ini_position[red_i][1] - 1))
#                         red_list.pos_piece_rect.topleft = red_list.pre_piece_rect.topleft
#                     elif ini_position[red_i][0] % 2 == 0:
#                         red_list.pre_piece_rect.topleft = (
#                         61 + 111.3 * (ini_position[red_i][0] - 2) / 2, 39 + 63.3 * (ini_position[red_i][1] - 1))
#                         red_list.pos_piece_rect.topleft = red_list.pre_piece_rect.topleft
#                     red_i = red_i + 1
#                     # 同步更新总库
#                     self.piece_group.add(red_list)
#             elif piece_name[:4] == "blue":
#                 for blue_list in self.blue_pieces:
#                     if ini_position[blue_j][0] % 2 == 1:
#                         blue_list.pre_piece_rect.topleft = (
#                         5 + 113 * (ini_position[blue_j][0] - 1) / 2, 7.5 + 63.3 * (ini_position[blue_j][1] - 1))
#                         blue_list.pos_piece_rect.topleft = blue_list.pre_piece_rect.topleft
#                         # print(ini_position[blue_j][0])
#                     elif ini_position[blue_j][0] % 2 == 0:
#                         blue_list.pre_piece_rect.topleft = (
#                         61 + 111.3 * (ini_position[blue_j][0] - 2) / 2, 39 + 63.3 * (ini_position[blue_j][1] - 1))
#                         blue_list.pos_piece_rect.topleft = blue_list.pre_piece_rect.topleft
#                         # print(ini_position[blue_j][0])
#                     blue_j = blue_j + 1
#                     # 同步更新总库
#                     self.piece_group.add(blue_list)
#         elif self.terrain.name == "mapAh":
#             if piece_name[:3] == "red":
#                 for red_list in self.red_pieces:
#                     if ini_position[red_i][0] % 2 == 1:  # 奇数行
#                         red_list.pre_piece_rect.topleft = (
#                             2 + 63 * (ini_position[red_i][1] - 1), 2.2 + 1.5 * 74 * (39 - ini_position[red_i][0]) / 2)
#                         red_list.pos_piece_rect.topleft = red_list.pre_piece_rect.topleft
#                     elif ini_position[red_i][0] % 2 == 0:  # 偶数行
#                         red_list.pre_piece_rect.topleft = (
#                             3 + 31.5 + 63 * (ini_position[red_i][1] - 1), 3 + 55.813 * (39 - ini_position[red_i][0]))
#                         red_list.pos_piece_rect.topleft = red_list.pre_piece_rect.topleft
#                     red_i = red_i + 1
#                     # 同步更新总库
#                     self.piece_group.add(red_list)
#             elif piece_name[:4] == "blue":
#                 for blue_list in self.blue_pieces:
#                     if ini_position[blue_j][0] % 2 == 1:  # 奇数行
#                         blue_list.pre_piece_rect.topleft = (
#                             2 + 63 * (ini_position[blue_j][1] - 1), 2.2 + 1.5 * 74 * (39 - ini_position[blue_j][0]) / 2)
#                         blue_list.pos_piece_rect.topleft = blue_list.pre_piece_rect.topleft
#                     elif ini_position[blue_j][0] % 2 == 0:  # 偶数行
#                         blue_list.pre_piece_rect.topleft = (
#                             3 + 31.5 + 63 * (ini_position[blue_j][1] - 1), 3 + 55.813 * (39 - ini_position[blue_j][0]))
#                         blue_list.pos_piece_rect.topleft = blue_list.pre_piece_rect.topleft
#                     blue_j = blue_j + 1
#                     # 同步更新总库
#                     self.piece_group.add(blue_list)
