import sys
import sqlite3
import xlrd
from importlib import import_module
from PyQt5.QtWidgets import QMessageBox,QLineEdit,QDialog,QLabel,QGraphicsItem,QSlider,QPushButton,QHBoxLayout,QVBoxLayout,QFileDialog,QApplication,QGraphicsTextItem,QGraphicsPixmapItem,QGraphicsPathItem,QGraphicsScene,QGraphicsView,QMainWindow,QMenuBar,QWidget,QAction
from PyQt5.QtGui import QColor,QBrush,QPainterPath,QPixmap,QFont
from PyQt5.Qt import Qt


# conn = pymysql.connect('test.db')
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
sql = 'SELECT * FROM 城镇居民地高程颜色'
cursor.execute(sql)
data = cursor.fetchall()
conn.close()

elevation_to_color ={}
for i in data:
    elevation_to_color[i[0]] = QColor(i[1],i[2],i[3])

class HexItem(QGraphicsPixmapItem):
    def __init__(self,co_x,co_y):
        super().__init__()
        self.co_x = co_x
        self.co_y = co_y
        self.setPos(*self.pix_pos)

    @property
    def pix_pos(self):
        if self.co_x % 2 == 0:
            topleft = (self.co_y * 54 + 27 - 20, self.co_x * 45 + 60 / 2 - 20)
        elif self.co_x % 2 == 1:
            topleft = (self.co_y * 54 + 54 - 20, self.co_x * 45 + 60 / 2 - 20)
        return topleft



class Flag(HexItem):
    def __init__(self,co_x,co_y):
        super().__init__(co_x,co_y)

        self.setPixmap(QPixmap('./resources/graphics/Control points.png'))
        self.setScale(0.07)

class Tank(HexItem):
    def __init__(self,co_x,co_y):
        super().__init__(co_x,co_y)
        self.move_history = [(self.co_x, self.co_y), (self.co_x, self.co_y)]
        self.action_history = []
        self.hex_history = []
        self.state_history =[]
        self.goal = (12, 24)

    def move_one_step(self, co_x, co_y):
        self.game_map = self.scene().views()[0]

        if not self.done:
            if 10 <= co_x <= 25 and 5 <= co_y <= 45:
                if (co_x, co_y) in self.game_map.get_neighbour(self.co_x, self.co_y):
                    print('Red tank Move_to: %s, %s' % (co_x, co_y))
                    self.co_x, self.co_y = co_x, co_y
                    self.action_history.append('机动')
                    self.hex_history.append((co_x, co_y))
                    self.change_to_move_state()
                    self.done = not self.done
                    self.move_history.append((co_x, co_y))
            else:
                print(co_x,co_y,'out of map')
                pass
        else:
            print('invalid red move operation')

class RTank(Tank):
    def __init__(self,co_x,co_y):
        super().__init__(co_x,co_y)
        self.setPixmap(QPixmap('./resources/graphics/piece/r_tank1.png'))

    def mousePressEvent(self, e):
        print(self.scene().views()[0].parent())




class BTank(Tank):
    def __init__(self,co_x,co_y):
        super().__init__(co_x,co_y)
        self.setPixmap(QPixmap('./resources/graphics/piece/b_tank1.png'))


class Scenario(object):
    def __init__(self):
        self.blue_tank_1 = BTank(15, 40)
        self.blue_tank_2 = BTank(16, 41)
        self.red_tank_1 = RTank(17, 7)
        self.red_tank_2 = RTank(18,8)
        self.goal = Flag(12,24)



class Hextile(QGraphicsPathItem):


    def __init__(self,room_id,map_id,map_id2,elevation,note,cond,obj_step,grid_id,grid_type,ground_id):
        super().__init__()

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        hex_path = QPainterPath()
        hex_path.moveTo(28,0)
        hex_path.lineTo(55,12)
        hex_path.lineTo(55,45)
        hex_path.lineTo(28,57)
        hex_path.lineTo(2,45)
        hex_path.lineTo(2,12)
        hex_path.lineTo(28,0)
        hex_path.closeSubpath()
        self.setPath(hex_path)
        ground_color = elevation_to_color[ground_id]
        brush = QBrush(ground_color)
        self.setBrush(brush)

        QGraphicsPixmapItem(QPixmap('./resources/graphics/Hex/Hex/cond{}.png'.format(str(int(cond)))), self)
        self.cond = int(cond)

        QGraphicsPixmapItem(QPixmap('./resources/graphics/Hex/Hex/{}.png'.format(str(int(grid_id)))), self)
        self.grid_id = int(grid_id)


        self.map_id = map_id
        self.ground_id = int(ground_id)

        text = QGraphicsTextItem(self.hex_str,self)
        text.setPos(10,0)
        text.setFont(QFont('arial',5))

        t = QGraphicsTextItem(str(int(ground_id)),self)
        t.setPos(15,28)
        t.setFont(QFont('arial',5))


        if self.map_id % 2 == 0:
            pos = (self.map_id % 10000 * 54 / 2, self.map_id // 10000 * 90)
        elif self.map_id % 2 == 1:
            pos = (self.map_id % 10000 * 54 / 2, self.map_id // 10000 * 90 + 45)

        self.setPos(*pos)


    def mousePressEvent(self, e):
        self.scene().views()[0].selected_item = self
        self.scene().views()[0].accept_signal()





    @property
    def hex_pos(self):
        x = self.map_id // 10000 * 2
        y = self.map_id % 10000
        if y % 2 == 0:
            y = y / 2
        else:
            y = y / 2 - 0.5
            x = x + 1
        return (int(x), int(y))

    @property
    def hex_str(self):
        x,y = self.hex_pos
        if x < 10:
            hex_x = '0' + str(x)
        else:
            hex_x = str(x)
        if y < 10:
            hex_y = '0' + str(y)
        else:
            hex_y = str(y)
        hex_id = hex_x + hex_y
        return hex_id




class GameMap(QGraphicsView):
    offline_potiential = {(1, 17): 8, (1, 20): 2, (1, 21): 3, (1, 22): 3, (1, 23): 5, (1, 25): 6, (1, 26): 5,
                          (1, 28): 4,
                          (1, 29): 7, (1, 30): 22, (1, 31): 1, (1, 36): 2, (1, 40): 2, (3, 14): 1, (2, 15): 2,
                          (2, 17): 1,
                          (3, 17): 3, (2, 18): 6, (2, 19): 5, (3, 19): 5, (3, 20): 1, (2, 21): 6, (3, 21): 6,
                          (2, 22): 23,
                          (3, 22): 38, (2, 23): 26, (3, 23): 62, (2, 24): 17, (3, 24): 39, (2, 25): 10, (3, 25): 2,
                          (2, 26): 3, (3, 26): 3, (3, 27): 32, (3, 28): 9, (2, 29): 2, (3, 29): 28, (2, 30): 1,
                          (3, 30): 10,
                          (2, 31): 11, (3, 31): 16, (2, 32): 2, (3, 32): 1, (3, 37): 2, (2, 38): 2, (3, 38): 2,
                          (5, 7): 2,
                          (5, 13): 6, (5, 15): 3, (5, 17): 3, (5, 18): 10, (4, 19): 4, (5, 19): 8, (4, 20): 4,
                          (5, 20): 27,
                          (4, 21): 14, (5, 21): 1, (5, 22): 2, (4, 23): 9, (5, 23): 7, (4, 24): 22, (5, 24): 3,
                          (4, 25): 4,
                          (5, 25): 3, (5, 26): 12, (4, 27): 21, (5, 27): 208, (4, 28): 15, (5, 28): 124, (4, 29): 5,
                          (5, 29): 23, (4, 30): 1, (5, 30): 24, (5, 31): 24, (4, 32): 5, (5, 32): 25, (4, 33): 27,
                          (5, 33): 12, (4, 34): 3, (5, 34): 10, (4, 35): 6, (5, 35): 2, (4, 36): 11, (5, 36): 19,
                          (4, 37): 34, (5, 37): 14, (7, 9): 4, (6, 10): 1, (6, 11): 2, (6, 12): 16, (6, 13): 17,
                          (6, 14): 8,
                          (7, 14): 1, (6, 15): 3, (6, 16): 3, (7, 16): 5, (6, 17): 29, (7, 17): 18, (6, 18): 4,
                          (7, 18): 38,
                          (6, 19): 9, (7, 19): 117, (7, 20): 19, (6, 21): 6, (7, 21): 27, (6, 22): 139, (7, 22): 7,
                          (6, 23): 73, (7, 23): 12, (6, 24): 195, (7, 24): 132, (6, 25): 42, (7, 25): 21, (6, 26): 36,
                          (7, 26): 32, (6, 27): 89, (7, 27): 19, (6, 28): 88, (7, 28): 140, (6, 29): 379, (7, 29): 54,
                          (6, 30): 41, (7, 30): 26, (6, 31): 12, (7, 31): 17, (6, 32): 13, (6, 33): 4, (6, 34): 3,
                          (6, 39): 1, (9, 10): 3, (8, 13): 1, (8, 15): 7, (9, 15): 6, (8, 16): 21, (9, 16): 2,
                          (8, 17): 32,
                          (9, 17): 55, (8, 18): 27, (9, 18): 81, (8, 19): 76, (9, 19): 12, (8, 20): 30, (9, 20): 39,
                          (8, 21): 17, (9, 21): 11, (8, 22): 48, (9, 22): 8, (8, 23): 54, (9, 23): 49, (8, 24): 306,
                          (9, 24): 13, (8, 25): 19, (9, 25): 1, (8, 26): 16, (9, 26): 2, (8, 27): 22, (9, 27): 33,
                          (8, 28): 88, (9, 28): 63, (8, 29): 61, (9, 29): 24, (8, 30): 10, (9, 30): 51, (8, 31): 38,
                          (8, 33): 3, (9, 33): 2, (8, 35): 1, (9, 39): 3, (11, 11): 13, (10, 12): 2, (11, 12): 6,
                          (10, 13): 8, (11, 13): 1, (10, 14): 5, (11, 14): 10, (10, 15): 1, (11, 15): 10, (10, 16): 20,
                          (11, 16): 11, (10, 17): 113, (11, 17): 18, (10, 18): 483, (11, 18): 4, (10, 19): 75,
                          (11, 19): 7,
                          (10, 20): 13, (11, 20): 15, (10, 21): 20, (11, 21): 5, (10, 22): 8, (11, 22): 1, (10, 23): 6,
                          (11, 23): 8, (10, 24): 21, (11, 24): 15, (10, 25): 5, (11, 25): 10, (10, 26): 13,
                          (11, 26): 164,
                          (10, 27): 36, (11, 27): 203, (10, 28): 180, (11, 28): 182, (10, 29): 50, (11, 29): 9,
                          (10, 30): 52, (11, 30): 6, (10, 31): 1, (11, 31): 1, (11, 32): 12, (11, 35): 1, (11, 36): 2,
                          (11, 37): 1, (10, 39): 4, (11, 40): 64, (10, 42): 3, (11, 42): 4, (10, 43): 4, (11, 43): 3,
                          (13, 8): 2, (12, 9): 5, (12, 10): 1, (13, 10): 3, (12, 11): 7, (13, 12): 3, (12, 13): 1,
                          (13, 13): 3, (12, 14): 2, (13, 14): 169, (12, 15): 3, (13, 15): 8, (12, 16): 19, (13, 16): 8,
                          (12, 17): 3, (13, 17): 3, (12, 18): 11, (13, 18): 6, (12, 19): 10, (13, 19): 42, (12, 20): 15,
                          (13, 20): 25, (12, 21): 14, (13, 21): 21, (13, 22): 12, (12, 23): 5, (13, 23): 26,
                          (12, 24): 28,
                          (13, 24): 42, (12, 25): 10, (13, 25): 136, (12, 26): 11, (13, 26): 287, (12, 27): 67,
                          (13, 27): 155, (12, 28): 71, (13, 28): 161, (12, 29): 81, (13, 29): 5, (12, 30): 62,
                          (13, 30): 145, (13, 31): 3, (12, 32): 1, (13, 32): 4, (13, 33): 4, (12, 34): 1, (12, 35): 1,
                          (13, 35): 45, (12, 36): 6, (13, 36): 10, (12, 37): 5, (13, 37): 9, (12, 39): 1, (13, 39): 8,
                          (12, 40): 3, (13, 41): 5, (13, 43): 1, (12, 44): 2, (13, 45): 7, (13, 47): 3, (15, 7): 8,
                          (14, 8): 1, (14, 10): 1, (14, 12): 1, (14, 13): 7, (15, 13): 18, (14, 14): 96, (15, 14): 377,
                          (14, 15): 1, (15, 15): 4, (14, 16): 9, (14, 17): 15, (15, 17): 23, (14, 18): 34, (15, 18): 24,
                          (14, 19): 57, (15, 19): 64, (14, 20): 80, (15, 20): 411, (14, 21): 66, (15, 21): 129,
                          (14, 22): 29, (15, 22): 186, (14, 23): 68, (15, 23): 366, (14, 24): 76, (15, 24): 465,
                          (14, 25): 90, (15, 25): 193, (14, 26): 108, (15, 26): 303, (14, 27): 54, (15, 27): 83,
                          (14, 28): 81, (15, 28): 125, (14, 29): 97, (15, 29): 6, (14, 30): 99, (15, 30): 8,
                          (14, 31): 5,
                          (15, 31): 12, (14, 32): 2, (14, 33): 5, (15, 34): 4, (14, 35): 17, (14, 36): 7, (14, 37): 3,
                          (14, 38): 2, (14, 39): 12, (15, 39): 5, (14, 40): 2, (15, 40): 5, (14, 41): 1, (15, 41): 1,
                          (14, 43): 2, (15, 43): 5, (14, 45): 2, (15, 45): 6, (14, 47): 7, (15, 48): 14, (17, 3): 6,
                          (17, 4): 1, (17, 5): 17, (17, 6): 3, (17, 8): 13, (17, 9): 37, (17, 10): 1, (16, 11): 1,
                          (17, 11): 2, (17, 12): 76, (16, 13): 15, (17, 13): 24, (16, 14): 1, (17, 14): 6, (16, 16): 4,
                          (17, 16): 7, (16, 17): 4, (17, 17): 2, (16, 18): 29, (17, 18): 31, (16, 19): 628,
                          (17, 19): 490,
                          (16, 20): 160, (17, 20): 73, (16, 21): 215, (17, 21): 159, (16, 22): 344, (17, 22): 314,
                          (16, 23): 789, (17, 23): 1643, (16, 24): 4515, (17, 24): 2662, (16, 25): 1118, (17, 25): 962,
                          (16, 26): 156, (17, 26): 210, (16, 27): 117, (17, 27): 139, (16, 28): 75, (17, 28): 105,
                          (16, 29): 65, (17, 29): 82, (16, 30): 7, (17, 30): 15, (16, 31): 5, (16, 32): 7, (17, 32): 4,
                          (16, 33): 1, (16, 34): 20, (17, 34): 45, (16, 35): 7, (17, 35): 8, (16, 36): 938, (17, 36): 3,
                          (17, 37): 14, (16, 38): 2, (17, 38): 2, (16, 39): 5, (17, 39): 5, (16, 40): 6, (17, 40): 6,
                          (16, 41): 1, (17, 41): 5, (17, 42): 2, (17, 43): 1, (17, 44): 9, (16, 45): 5, (16, 46): 1,
                          (17, 46): 1, (16, 47): 3, (17, 47): 1, (16, 48): 12, (17, 48): 13, (16, 49): 10, (16, 50): 3,
                          (19, 0): 1, (18, 1): 4, (19, 1): 1, (18, 2): 3, (19, 2): 9, (18, 3): 3, (19, 3): 6,
                          (18, 4): 9,
                          (19, 4): 9, (18, 5): 9, (19, 5): 11, (18, 6): 9, (19, 6): 1, (18, 8): 7, (19, 8): 15,
                          (18, 9): 19,
                          (18, 10): 1, (19, 10): 10, (18, 11): 3, (19, 11): 60, (18, 12): 3, (19, 12): 17, (18, 13): 1,
                          (19, 13): 4, (18, 14): 5, (19, 14): 24, (18, 15): 3, (19, 15): 22, (18, 16): 3, (19, 16): 21,
                          (18, 17): 14, (19, 17): 26, (18, 18): 19, (19, 18): 24, (18, 19): 51, (19, 19): 136,
                          (18, 20): 412, (19, 20): 98, (18, 21): 104, (19, 21): 188, (18, 22): 302, (19, 22): 601,
                          (18, 23): 391, (19, 23): 423, (18, 24): 582, (19, 24): 678, (18, 25): 2682, (19, 25): 1241,
                          (18, 26): 586, (19, 26): 206, (18, 27): 191, (19, 27): 64, (18, 28): 86, (19, 28): 375,
                          (18, 29): 282, (19, 29): 21, (18, 30): 17, (19, 30): 4, (18, 31): 2, (19, 31): 20,
                          (18, 32): 5,
                          (19, 32): 15, (18, 33): 12, (19, 33): 6, (18, 34): 19, (19, 34): 15, (18, 35): 44,
                          (19, 35): 100,
                          (18, 36): 35, (19, 36): 1, (18, 37): 6, (19, 37): 3, (18, 38): 18, (19, 38): 1, (18, 39): 2,
                          (18, 40): 11, (18, 41): 4, (18, 42): 5, (18, 43): 1, (18, 44): 2, (19, 45): 1, (18, 46): 5,
                          (19, 46): 1, (18, 47): 2, (19, 47): 3, (18, 50): 3, (18, 51): 3, (18, 52): 2, (19, 52): 1,
                          (21, 0): 2, (21, 1): 2, (20, 3): 1, (21, 3): 2, (20, 4): 6, (21, 4): 2, (20, 5): 6,
                          (21, 5): 4,
                          (20, 6): 4, (20, 7): 8, (20, 8): 1, (20, 11): 5, (20, 12): 259, (21, 12): 235, (20, 13): 7,
                          (21, 13): 4, (20, 14): 6, (21, 14): 10, (20, 15): 18, (21, 15): 25, (20, 16): 9, (21, 16): 15,
                          (20, 17): 6, (21, 17): 13, (20, 18): 9, (21, 18): 22, (20, 19): 36, (21, 19): 30,
                          (20, 20): 128,
                          (21, 20): 122, (20, 21): 121, (21, 21): 88, (20, 22): 195, (21, 22): 155, (20, 23): 377,
                          (21, 23): 598, (20, 24): 536, (21, 24): 2962, (20, 25): 1041, (21, 25): 642, (20, 26): 534,
                          (21, 26): 560, (20, 27): 577, (21, 27): 44, (20, 28): 398, (21, 28): 18, (20, 29): 23,
                          (21, 29): 16, (20, 30): 7, (21, 30): 9, (20, 31): 1, (21, 31): 3, (20, 32): 9, (21, 32): 16,
                          (20, 33): 13, (21, 33): 14, (20, 34): 10, (21, 34): 14, (20, 35): 162, (21, 35): 11,
                          (20, 36): 1,
                          (21, 36): 19, (21, 37): 7, (21, 38): 2, (20, 39): 14, (21, 39): 7, (20, 41): 5, (20, 42): 2,
                          (21, 44): 1, (20, 45): 7, (20, 46): 5, (20, 51): 1, (20, 52): 1, (20, 53): 2, (22, 3): 7,
                          (23, 4): 3, (23, 5): 2, (23, 6): 2, (22, 7): 7, (23, 7): 5, (23, 8): 1, (22, 9): 1,
                          (23, 9): 5,
                          (22, 10): 2, (23, 10): 4, (22, 11): 3, (23, 11): 3, (22, 12): 2, (23, 12): 3, (23, 13): 11,
                          (22, 14): 12, (23, 14): 8, (22, 15): 8, (23, 15): 87, (22, 16): 4, (23, 16): 19,
                          (22, 17): 104,
                          (23, 17): 28, (22, 18): 30, (23, 18): 26, (22, 19): 23, (23, 19): 53, (22, 20): 230,
                          (23, 20): 46,
                          (22, 21): 58, (23, 21): 179, (22, 22): 81, (23, 22): 262, (22, 23): 264, (23, 23): 335,
                          (22, 24): 1207, (23, 24): 175, (22, 25): 541, (23, 25): 198, (22, 26): 164, (23, 26): 231,
                          (22, 27): 271, (23, 27): 363, (22, 28): 20, (23, 28): 22, (22, 29): 7, (23, 29): 8,
                          (22, 30): 1,
                          (23, 30): 3, (22, 31): 1, (23, 31): 3, (22, 32): 5, (23, 32): 6, (23, 33): 8, (22, 34): 3,
                          (23, 34): 5, (23, 35): 4, (22, 36): 4, (23, 36): 3, (22, 37): 2, (23, 38): 3, (23, 39): 26,
                          (22, 44): 3, (23, 44): 6, (22, 46): 1, (23, 49): 3, (24, 1): 1, (24, 4): 2, (24, 6): 1,
                          (25, 6): 1, (24, 7): 3, (24, 8): 14, (24, 9): 3, (24, 10): 4, (25, 10): 2, (24, 11): 7,
                          (25, 11): 5, (24, 12): 7, (25, 12): 1, (24, 13): 2, (25, 13): 12, (24, 14): 3, (25, 14): 5,
                          (24, 15): 22, (25, 15): 6, (24, 16): 8, (25, 16): 8, (24, 17): 9, (25, 17): 12, (24, 18): 11,
                          (25, 18): 39, (24, 19): 19, (25, 19): 37, (24, 20): 24, (25, 20): 92, (24, 21): 23,
                          (25, 21): 37,
                          (24, 22): 28, (25, 22): 29, (24, 23): 147, (25, 23): 28, (24, 24): 30, (25, 24): 47,
                          (24, 25): 64,
                          (25, 25): 93, (24, 26): 139, (25, 26): 164, (24, 27): 192, (25, 27): 34, (24, 28): 19,
                          (25, 28): 346, (24, 29): 11, (25, 29): 16, (24, 30): 5, (25, 30): 5, (24, 31): 3, (25, 32): 4,
                          (25, 33): 1, (24, 34): 3, (25, 34): 2, (25, 35): 4, (25, 36): 8, (24, 37): 2, (25, 37): 4,
                          (24, 38): 1, (25, 38): 3, (24, 39): 9, (25, 39): 4, (24, 40): 1, (25, 40): 11, (24, 41): 6,
                          (25, 44): 2, (25, 45): 2, (25, 51): 1, (26, 5): 2, (26, 7): 3, (26, 12): 5, (27, 12): 2,
                          (27, 13): 2, (27, 14): 1, (26, 15): 5, (27, 15): 8, (26, 16): 12, (26, 17): 11, (27, 17): 47,
                          (26, 18): 16, (27, 18): 6, (26, 19): 1, (27, 19): 29, (26, 20): 531, (27, 20): 166,
                          (26, 21): 18,
                          (27, 21): 16, (26, 22): 14, (27, 22): 20, (26, 23): 9, (27, 23): 15, (26, 24): 29,
                          (27, 24): 33,
                          (26, 25): 74, (27, 25): 106, (26, 26): 99, (27, 26): 132, (26, 27): 209, (27, 27): 16,
                          (26, 28): 18, (27, 28): 5, (26, 29): 9, (26, 30): 5, (27, 30): 3, (27, 31): 1, (26, 32): 2,
                          (27, 32): 7, (26, 33): 9, (27, 33): 1, (26, 35): 94, (27, 35): 10, (27, 37): 1, (26, 42): 3,
                          (27, 43): 1, (27, 49): 2, (28, 12): 11, (28, 13): 10, (28, 14): 12, (29, 14): 3, (29, 15): 17,
                          (28, 16): 23, (29, 16): 6, (28, 17): 6, (29, 17): 4, (28, 18): 31, (29, 18): 42, (28, 19): 58,
                          (29, 19): 26, (28, 20): 11, (29, 20): 50, (28, 21): 221, (29, 21): 123, (28, 22): 45,
                          (29, 22): 53, (28, 23): 8, (29, 23): 24, (28, 24): 16, (29, 24): 94, (28, 25): 44,
                          (29, 25): 183,
                          (28, 26): 202, (29, 26): 32, (28, 27): 241, (29, 27): 8, (28, 28): 274, (29, 28): 33,
                          (28, 29): 22, (29, 29): 329, (28, 30): 5, (29, 30): 30, (28, 31): 1, (29, 31): 14,
                          (28, 32): 11,
                          (29, 32): 6, (28, 33): 8, (28, 34): 9, (29, 34): 5, (28, 35): 9, (28, 36): 60, (29, 36): 11,
                          (29, 37): 11, (28, 38): 5, (29, 38): 1, (29, 39): 1, (28, 40): 2, (29, 40): 1, (28, 42): 1,
                          (29, 42): 5, (28, 43): 12, (28, 44): 1, (29, 44): 1, (31, 14): 4, (30, 16): 2, (31, 17): 1,
                          (30, 18): 1, (30, 19): 23, (31, 19): 7, (30, 20): 10, (31, 20): 5, (30, 21): 11,
                          (31, 21): 105,
                          (30, 22): 116, (31, 22): 64, (30, 23): 106, (31, 23): 9, (30, 24): 161, (31, 24): 9,
                          (30, 25): 12,
                          (31, 25): 13, (30, 26): 15, (31, 27): 2, (30, 28): 3, (30, 29): 1, (31, 29): 2, (30, 30): 3,
                          (31, 30): 5, (30, 31): 35, (31, 31): 17, (31, 32): 4, (30, 33): 9, (31, 34): 1, (30, 35): 3,
                          (31, 35): 1, (30, 36): 1, (31, 36): 1, (31, 37): 2, (31, 39): 2, (30, 40): 4, (30, 51): 1,
                          (33, 15): 5, (32, 16): 3, (33, 16): 3, (32, 17): 4, (33, 17): 51, (33, 18): 3, (32, 19): 5,
                          (33, 19): 9, (32, 20): 12, (33, 20): 3, (32, 21): 7, (33, 21): 5, (32, 22): 67, (33, 22): 22,
                          (33, 23): 5, (32, 24): 2, (32, 26): 5, (33, 26): 1, (32, 28): 5, (33, 29): 2, (33, 30): 53,
                          (32, 31): 8, (32, 32): 2, (33, 32): 3, (32, 33): 3, (32, 35): 1, (32, 36): 4, (33, 36): 1,
                          (32, 37): 2, (32, 38): 2, (33, 40): 1, (33, 42): 2, (33, 43): 3, (34, 11): 1, (34, 15): 2,
                          (35, 15): 7, (35, 16): 4, (34, 17): 2, (35, 17): 1, (34, 18): 10, (34, 19): 1, (35, 19): 4,
                          (34, 20): 6, (34, 22): 30, (34, 23): 7, (34, 24): 2, (35, 24): 3, (35, 27): 3, (35, 29): 3,
                          (34, 30): 1, (35, 30): 3, (34, 31): 5, (35, 31): 4, (34, 32): 4, (35, 32): 4, (35, 36): 1,
                          (34, 38): 2, (34, 40): 2, (35, 40): 1, (36, 14): 9, (36, 15): 4, (36, 16): 3, (37, 17): 65,
                          (36, 18): 4, (37, 18): 60, (37, 19): 4, (36, 20): 2, (37, 21): 1, (36, 22): 1, (36, 23): 4,
                          (37, 23): 15, (36, 24): 2, (37, 24): 1, (36, 25): 3, (37, 29): 4, (36, 30): 9, (37, 30): 5,
                          (36, 31): 3, (36, 32): 3, (37, 32): 2, (37, 33): 1, (36, 41): 2, (39, 15): 1, (39, 16): 4,
                          (38, 17): 1, (39, 17): 2, (38, 18): 17, (39, 18): 68, (38, 19): 5, (39, 19): 1, (38, 20): 10,
                          (39, 20): 6, (38, 23): 5, (38, 24): 4, (38, 25): 4, (38, 26): 3, (38, 29): 1, (39, 31): 5,
                          (39, 32): 2, (38, 33): 16, (39, 33): 2, (38, 34): 2, (39, 34): 1, (39, 36): 1, (38, 37): 1,
                          (38, 39): 1, (41, 15): 1, (41, 16): 2, (40, 17): 4, (40, 18): 1, (41, 18): 4, (40, 19): 4,
                          (41, 23): 2, (40, 24): 1, (41, 24): 5, (41, 26): 3, (41, 27): 1, (41, 28): 1, (40, 29): 2,
                          (42, 17): 2, (43, 18): 1, (42, 21): 1, (42, 27): 2, (42, 28): 1, (42, 41): 3, (45, 11): 1,
                          (44, 12): 2, (44, 15): 1, (45, 15): 1, (44, 19): 3, (46, 9): 1, (47, 10): 3, (47, 19): 1,
                          (46, 21): 2, (48, 13): 1, (48, 18): 1, (48, 20): 2, (48, 21): 2}
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 3000, 3000)
        self.setScene(self.scene)
        # '01城镇居民地', '02岛上台地', '03高原通道','05山岳丛林地', '06水网稻田地'
        data = xlrd.open_workbook('./resources/game_maps/01城镇居民地.XLS')
        game_map_data = data.sheet_by_index(0)

        self.load_map(game_map_data)

        self.selected_item = None

    def get_neighbour(self, co_x, co_y):
        neighbour = []
        if co_x % 2 == 0:
            neighbour = [(co_x, co_y - 1), (co_x, co_y + 1), (co_x - 1, co_y - 1), (co_x - 1, co_y),
                         (co_x + 1, co_y - 1), (co_x + 1, co_y)]
        if co_x % 2 == 1:
            neighbour = [(co_x, co_y - 1), (co_x, co_y + 1), (co_x - 1, co_y), (co_x - 1, co_y + 1), (co_x + 1, co_y),
                         (co_x + 1, co_y + 1)]
        return neighbour

    def get_distance_between_hex(self, hex_1_x, hex_1_y, hex_2_x, hex_2_y):
        def oddr_to_cube(row, col):

            x = col - (row - (row & 1)) / 2
            z = row
            y = -x - z
            return (x, y, z)

        start = oddr_to_cube(hex_1_x, hex_1_y)
        end = oddr_to_cube(hex_2_x, hex_2_y)
        return int(max(abs(start[0] - end[0]), abs(start[1] - end[1]), abs(start[2] - end[2])))

    def load_map(self,map_data):
        for i in range(map_data.nrows):
            d = map_data.cell_value
            try:
                h = Hextile(d(i,0),d(i,1),d(i,2),d(i,3),d(i,4),d(i,5),d(i,6),d(i,7),d(i,8),d(i,9))
                self.scene.addItem(h)
            except Exception as e:
                print(e)


    def load_piece(self,cls):
        self.scene.addItem(cls.red_tank_1)
        self.scene.addItem(cls.red_tank_2)
        self.scene.addItem(cls.blue_tank_1)
        self.scene.addItem(cls.blue_tank_2)
        self.scene.addItem(cls.goal)





class Wargame_env(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('地图编辑器')
        self.resize(2000,1000)

        menu_file = self.menuBar().addMenu('文件')
        open_action = QAction('打开',self)
        menu_file.addAction(open_action)
        open_action.triggered.connect(self.open_file)


        l = QHBoxLayout()
        self.game_map = GameMap()
        self.control = QWidget()
        l.addWidget(self.game_map)
        l.addWidget(self.control)
        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)


        v = QVBoxLayout()
        self.control.setLayout(v)

        l1 = QLabel('尺寸调整')
        v.addWidget(l1)

        s = QSlider(Qt.Horizontal)
        v.addWidget(s)
        s.setMinimum(6)
        s.setMaximum(20)
        s.setValue(10)
        s.setTickInterval(2)
        s.setTickPosition(QSlider.TicksBelow)
        s.valueChanged.connect(self.change_scale)

        self.l2 = QLabel('六角格坐标: ')
        v.addWidget(self.l2)

        l3 = QLabel('高程')
        v.addWidget(l3)

        self.l4 = QLineEdit('')
        v.addWidget(self.l4)

        l4 = QLabel('地形')
        v.addWidget(l4)


        self.scenario = Scenario()
        self.game_map.load_piece(self.scenario)



    def reset(self):
        self.scenario = Scenario()
        self.game_map.load_piece(self.scenario)


    def change_scale(self,v):
        former_scale = self.game_map.transform().m11()
        self.game_map.scale(v/10.0/former_scale,v/10.0/former_scale)




    def open_file(self):
        self.q = QDialog()
        b1 = QPushButton('加载1号选手')
        b2 = QPushButton('加载2号选手')
        self.q.l1 = QLabel('')
        self.q.l2 = QLabel('')
        b3 = QPushButton('开始模拟')
        v = QVBoxLayout()
        v.addWidget(b1)
        v.addWidget(self.q.l1)
        v.addWidget(b2)
        v.addWidget(self.q.l2)
        v.addWidget(b3)
        self.q.setLayout(v)
        b1.pressed.connect(self.choose_file_1)
        b2.pressed.connect(self.choose_file_2)
        b3.pressed.connect(self.wargame_run)
        self.q.exec()

    def choose_file_1(self):
        file,ok = QFileDialog.getOpenFileName(self, "打开",'.',"python files (*.py)")
        self.q.l1.setText(file)
        self.f1 = file

    def choose_file_2(self):
        file,ok = QFileDialog.getOpenFileName(self, "打开",'.',"python files (*.py)")
        self.q.l2.setText(file)
        self.f2 = file

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
        red_tank_1 = self.scenario.red_tank_1
        red_tank_2 = self.scenario.red_tank_2
        blue_tank_1 = self.scenario.blue_tank_1
        blue_tank_2 = self.scenario.blue_tank_2
        if red_tank_1.num <= 0:
            red_tank_1.num = 0
        if blue_tank_1.num <= 0:
            blue_tank_1.num = 0
        if red_tank_2.num <= 0:
            red_tank_2.num = 0
        if blue_tank_2.num <= 0:
            blue_tank_2.num = 0
        if (blue_tank_1.co_x == blue_tank_1.goal[0] and blue_tank_1.co_y == blue_tank_1.goal[1]) or (
                blue_tank_2.co_x == blue_tank_2.goal[0] and blue_tank_2.co_y == blue_tank_2.goal[1]):
            print('Blue Win,Goal')
            self.scenario.state_controlpoint = 'blue_control'
            self.blue_win_times += 1
            self.total_episodes += 1

            self.red_kill_score += (3 - blue_tank_1.num) * 10
            self.red_get_goal_score += 0
            self.red_survive_score += red_tank_1.num * 9

            self.blue_kill_score = (3 - red_tank_1.num) * 9
            self.blue_get_goal_score += 80
            self.blue_survive_score = blue_tank_1.num * 10

            return True
        elif (red_tank_1.co_x == red_tank_1.goal[0] and red_tank_1.co_y == red_tank_1.goal[1]) or (
                red_tank_2.co_x == red_tank_2.goal[0] and red_tank_2.co_y == red_tank_2.goal[1]):
            print('Red Win,Goal')
            self.scenario.state_controlpoint = 'red_control'
            self.red_win_times += 1
            self.total_episodes += 1

            self.red_kill_score += (3 - blue_tank_1.num) * 10
            self.red_get_goal_score += 80
            self.red_survive_score += red_tank_1.num * 9

            self.blue_kill_score = (3 - red_tank_1.num) * 9
            self.blue_get_goal_score += 0
            self.blue_survive_score = blue_tank_1.num * 10

            return True
        elif red_tank_1.num == 0 and red_tank_2.num == 0:
            self.blue_win_times += 1
            self.total_episodes += 1
            self.red_kill_score += (3 - blue_tank_1.num) * 10
            self.red_kill_score += (3 - blue_tank_2.num) * 10
            self.red_get_goal_score += 0
            self.red_survive_score += red_tank_1.num * 9
            self.red_survive_score += red_tank_2.num * 9

            self.blue_kill_score = (3 - red_tank_1.num) * 9
            self.blue_kill_score = (3 - red_tank_2.num) * 9
            self.blue_get_goal_score += 80
            self.blue_survive_score += blue_tank_1.num * 10
            self.blue_survive_score += blue_tank_2.num * 10

            print('Blue Win,Kill All')
            return True
        elif blue_tank_1.num == 0 and blue_tank_2.num == 0:
            self.red_win_times += 1
            self.total_episodes += 1

            self.red_kill_score += (3 - blue_tank_1.num) * 10
            self.red_kill_score += (3 - blue_tank_2.num) * 10
            self.red_get_goal_score += 80
            self.red_survive_score += red_tank_1.num * 9
            self.red_survive_score += red_tank_2.num * 9

            self.blue_kill_score += (3 - red_tank_1.num) * 9
            self.blue_kill_score += (3 - red_tank_2.num) * 9
            self.blue_get_goal_score += 0
            self.blue_survive_score += blue_tank_1.num * 10
            self.blue_survive_score += blue_tank_2.num * 10

            print('Red Win,Kill All')
            return True
        else:
            return False


    def wargame_run(self):
        self.q.close()
        a = self.f1.rsplit('/', 1)
        path = a[0]
        f = a[1].rsplit('.', 1)
        sys.path.append(path)
        player_1 = import_module(f[0])

        a = self.f2.rsplit('/', 1)
        path = a[0]
        f = a[1].rsplit('.', 1)
        sys.path.append(path)
        player_2 = import_module(f[0])

        self.p1_name = player_1.NAME
        self.p2_name = player_2.NAME

        # 上下半场的总局数
        first_half_episodes = 100
        second_half_episodes = 100
        first_episode_num = 0
        second_episode_num = 0

        self.steps = 0


        while first_episode_num <= first_half_episodes:

            self.steps += 1
            self.check_indirect_fire('red')
            # 打开红方行动开关，关闭蓝方行动开关
            self.scenario.red_tank_1.done = False
            self.scenario.red_tank_2.done = False
            self.scenario.blue_tank_1.done = True
            self.scenario.blue_tank_2.done = True
            player_1.red_choose_action(self)

            # 判断是否取胜,重置
            if self.check_win():
                first_episode_num += 1
                print("上半场： 第%s episode 第%s step" % (first_episode_num, self.steps))
                self.reset()
                print("First Half %s :Red Win %s,Blue Win %s" % (
                    first_episode_num, self.red_win_times, self.blue_win_times))
            else:


                self.check_indirect_fire('blue')
                # 打开蓝方行动开关，关闭红方行动开关
                self.scenario.red_tank_1.done = True
                self.scenario.red_tank_2.done = True
                self.scenario.blue_tank_1.done = False
                self.scenario.blue_tank_2.done = False
                player_2.blue_choose_action(self)

                # # 判断是否取胜,重置
                if self.check_win():
                    first_episode_num += 1
                    self.reset()
                    print("First Half %s :Red Win %s,Blue Win %s" % (
                        first_episode_num, self.red_win_times, self.blue_win_times))

        print('上半场 End')

        # --------------------上半场所对抗结束，下半场所开始-------------------------------------------------------------------
        m = QMessageBox('hello world')
        self.steps = 0
        while second_episode_num <= second_half_episodes:

            self.steps += 1
            print("Second Half,episode:%s, Step:%s" % (second_episode_num, self.steps))
            self.check_indirect_fire('red')

            # 下半场的一局结束，重置
            if self.check_win():
                second_episode_num += 1
                self.reset()
                print("Second Half %s :Red Win %s,Blue Win %s" % (
                    second_episode_num, self.red_win_times, self.blue_win_times))
            else:
                self.scenario.red_tank_1.done = False
                self.scenario.red_tank_2.done = False
                self.scenario.blue_tank_1.done = True
                self.scenario.blue_tank_2.done = True

                self.check_indirect_fire('blue')

                if self.check_win():
                    second_episode_num += 1
                    self.reset()
                    print("Second Half %s :Red Win %s,Blue Win %s" % (
                        second_episode_num, self.red_win_times, self.blue_win_times))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    wargame_env = Wargame_env()
    wargame_env.show()
    sys.exit(app.exec())