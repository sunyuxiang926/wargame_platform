import sys
import sqlite3
import xlrd
from PyQt5.QtWidgets import QPlainTextEdit, QComboBox, QTabWidget, QTableWidgetItem, QLineEdit, QDialog, QLabel, \
    QGraphicsItem, QSlider, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QApplication, QGraphicsTextItem, \
    QGraphicsPixmapItem, QGraphicsPathItem, QGraphicsScene, QGraphicsView, QMainWindow, QMenuBar, QWidget, QAction
from PyQt5.QtGui import QColor, QBrush, QPainterPath, QPixmap, QPalette, QFont, QIcon
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.Qt import Qt
def pos_to_hex_pos(x, y):
    grid_width = 54
    grid_height = int(60 / 4.0 * 3)
    half_width = int(54 / 2.0)
    row = int(y / grid_height)
    row_is_odd = (row % 2 == 1)
    rel_y = y - (row * grid_height)
    if row_is_odd:
        column = int((x - half_width) / grid_width)
        rel_x = (x - (column * grid_width)) - half_width
    else:
        column = int(x / grid_width)
        rel_x = x - (column * grid_width)
    a = 60 / 4.0
    m = a / half_width
    if rel_y < -m * rel_x + a:
        row -= 1
        if not row_is_odd:
            column -= 1
    elif rel_y < m * rel_x - a:
        row -= 1
        if row_is_odd:
            column += 1
    if row < 10:
        row = '0' + str(row)
    else:
        row = str(row)
    if column < 10:
        column = '0' + str(column)
    else:
        column = str(column)
    return row + column
def hex_pos_to_pos(hex_pos):
    hex_a, hex_b = int(hex_pos[:2]), int(hex_pos[2:])
    if hex_a % 2 == 0:
        x = hex_b * 54 + 9
        y = hex_a * 45 + 9
    elif hex_a % 2 == 1:
        x = hex_b * 54 + 27 + 9
        y = hex_a * 45 + 9
    return x, y
def get_distance(hex_1, hex_2):
    hex_1_x, hex_1_y = int(hex_1[:2]), int(hex_1[2:])
    hex_2_x, hex_2_y = int(hex_2[:2]), int(hex_2[2:])

    def oddr_to_cube(row, col):
        x = col - (row - (row & 1)) / 2
        z = row
        y = -x - z
        return (x, y, z)
    start = oddr_to_cube(hex_1_x, hex_1_y)
    end = oddr_to_cube(hex_2_x, hex_2_y)
    return int(max(abs(start[0] - end[0]), abs(start[1] - end[1]), abs(start[2] - end[2])))
def get_hexes_between_hex(hex_1, hex_2):
    point_1_x, point_1_y = hex_pos_to_pos(hex_1)
    point_2_x, point_2_y = hex_pos_to_pos(hex_2)
    n = get_distance(hex_1, hex_2)
    delta_x = (point_2_x - point_1_x) / n
    delta_y = (point_2_y - point_1_y) / n
    hexes = []
    for i in range(n + 1):
        hex = pos_to_hex_pos(point_1_x + i * delta_x, point_1_y + i * delta_y)
        if hex not in hexes:
            hexes.append(hex)
    return hexes
def check_observation(hex_1, hex_2, data):
    hexes = get_hexes_between_hex(hex_1, hex_2)
    elevation = []
    for i in hexes:
        if data[i].ground_id == 3:
            return '不通视'
        elevation.append(data[i].ground_id)
    if max(elevation) > max(elevation[0], elevation[-1]):
        return '不通视'
    else:
        return '通视'
class MyObject(QObject):
    sig = pyqtSignal(str)
class Piece(QGraphicsPixmapItem):
    def __init__(self, name, hex_pos):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.name = name
        self.setScale(0.5)
        self.e = MyObject()
        self.hex_pos = hex_pos
        hex_a, hex_b = int(self.hex_pos[:2]), int(self.hex_pos[2:])
        pos = ()
        if hex_a % 2 == 0:
            pos = (hex_b * 54 + 9, hex_a * 45 + 9)
        elif hex_a % 2 == 1:
            pos = (hex_b * 54 + 27 + 9, hex_a * 45 + 9)
        self.setPos(*pos)
        self.e.sig.connect(self.move)

    def move(self, hex_pos):
        pos = ()
        hex_a, hex_b = int(hex_pos[:2]), int(hex_pos[2:])
        if hex_a % 2 == 0:
            pos = (hex_b * 54 + 9, hex_a * 45 + 18)
        elif hex_a % 2 == 1:
            pos = (hex_b * 54 + 27 + 9, hex_a * 45 + 18)
        self.setPos(*pos)
class ControlPoint(Piece):
    def __init__(self, name, hex_pos):
        super().__init__(name, hex_pos)
        self.setPixmap(QPixmap('./resources/graphics/qtimg/Control points.png'))
class RTank(Piece):
    def __init__(self, name, hex_pos):
        super().__init__(name, hex_pos)
        p = QPixmap('./resources/graphics/qtimg/UNITs1_26.jpg')
        self.setPixmap(p)
class BTank(Piece):
    def __init__(self, name, hex_pos):
        super().__init__(name, hex_pos)
        p = QPixmap('./resources/graphics/qtimg/UNITs2_60.jpg')
        self.setPixmap(p)
class Hextile(QGraphicsPathItem):
    def __init__(self, room_id, map_id, map_id2, elevation, note, cond, obj_step, grid_id, grid_type, ground_id):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        hex_path = QPainterPath()
        hex_path.moveTo(28, 0)
        hex_path.lineTo(55, 12)
        hex_path.lineTo(55, 45)
        hex_path.lineTo(28, 57)
        hex_path.lineTo(2, 45)
        hex_path.lineTo(2, 12)
        hex_path.lineTo(28, 0)
        hex_path.closeSubpath()
        self.setPath(hex_path)
        self.ground_color = ground_id
        QGraphicsPixmapItem(QPixmap('./resources/graphics/Hex/Hex/dixing{}.png'.format(str(int(ground_id)))), self)
        QGraphicsPixmapItem(QPixmap('./resources/graphics/Hex/Hex/cond{}.png'.format(str(int(cond)))), self)
        self.cond = int(cond)
        QGraphicsPixmapItem(QPixmap('./resources/graphics/Hex/Hex/{}.png'.format(str(int(grid_id)))), self)
        self.grid_id = int(grid_id)
        self.map_id = map_id
        self.ground_id = int(ground_id)
        text = QGraphicsTextItem(self.hex_str, self)
        text.setPos(10, 0)
        text.setFont(QFont('arial', 5))
        t = QGraphicsTextItem(str(int(ground_id)), self)
        t.setPos(15, 28)
        t.setFont(QFont('arial', 5))
        if self.map_id % 2 == 0:
            pos = (self.map_id % 10000 * 54 / 2, self.map_id // 10000 * 90)
        elif self.map_id % 2 == 1:
            pos = (self.map_id % 10000 * 54 / 2, self.map_id // 10000 * 90 + 45)
        self.setPos(*pos)
    def paintcolor(self, color):
        brush = QBrush(color)
        self.setBrush(brush)
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
        x, y = self.hex_pos
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
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 3000, 3000)
        self.setScene(self.scene)
        self.selected_item = None
        self.hexes = {}
        self.data = None
        import xlrd
        data = xlrd.open_workbook('./resources/game_maps/01 城镇居民地.xls')
        game_map_data = data.sheet_by_index(0)
        self.load_map(game_map_data)
        self.e = MyObject()
        self.r1 = RTank('tank', '1707')
        self.r2 = RTank('tank', '1808')
        self.b1 = BTank('tank', '1540')
        self.b2 = BTank('tank', '1641')
        self.c1 = ControlPoint('cp', '1224')
        self.scene.addItem(self.r1)
        self.scene.addItem(self.r2)
        self.scene.addItem(self.b1)
        self.scene.addItem(self.b2)
        self.scene.addItem(self.c1)
    def load_map(self, map_data):
        for i in range(map_data.nrows):
            d = map_data.cell_value
            self.data = d
            try:
                h = Hextile(d(i, 0), d(i, 1), d(i, 2), d(i, 3), d(i, 4), d(i, 5), d(i, 6), d(i, 7), d(i, 8), d(i, 9))
                self.hexes[h.hex_str] = h
                self.scene.addItem(self.hexes[h.hex_str])
            except Exception as e:
                print(e)
class ScenarioEditor(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('局势分析器')
        self.resize(2000, 1000)
        self.setWindowIcon(QIcon('tank.png'))
        self.setStyleSheet('QPushButton{color:black;background-color:white;border-radius:15px;border: 3px solid blue}')
        l = QHBoxLayout()
        self.game_map = GameMap()
        self.t = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.t.addTab(self.tab1, "红方局势")
        self.t.addTab(self.tab2, "蓝方局势")
        self.t.addTab(self.tab3, "辅助工具")
        v1 = QVBoxLayout()
        self.r_b1 = QPushButton('我情分析')
        self.r_b1.pressed.connect(self.show_red_message)
        self.r_p1 = QPlainTextEdit()
        self.r_b2 = QPushButton('敌情分析')
        self.r_b2.pressed.connect(self.show_blue_message)
        self.r_p2 = QPlainTextEdit()
        self.r_b3 = QPushButton('作战提示')
        self.r_b3.pressed.connect(self.show_battle_suggest)
        self.r_p3 = QPlainTextEdit()
        v1.addWidget(self.r_b1)
        v1.addWidget(self.r_p1)
        v1.addWidget(self.r_b2)
        v1.addWidget(self.r_p2)
        v1.addWidget(self.r_b3)
        v1.addWidget(self.r_p3)
        self.tab1.setLayout(v1)
        v2 = QVBoxLayout()
        self.r_b4 = QPushButton('我情分析')
        self.r_b4.pressed.connect(self.show_blue_message)
        self.r_p4 = QPlainTextEdit()
        self.r_b5 = QPushButton('敌情分析')
        self.r_b5.pressed.connect(self.show_red_message)
        self.r_p5 = QPlainTextEdit()
        self.r_b6 = QPushButton('作战提示')
        self.r_b6.pressed.connect(self.show_battle_suggest)
        self.r_p6 = QPlainTextEdit()
        v2.addWidget(self.r_b4)
        v2.addWidget(self.r_p4)
        v2.addWidget(self.r_b5)
        v2.addWidget(self.r_p5)
        v2.addWidget(self.r_b6)
        v2.addWidget(self.r_p6)
        self.tab2.setLayout(v2)
        v = QVBoxLayout()
        l1 = QLabel('通视分析')
        v.addWidget(l1)
        self.text1 = QLineEdit()
        self.text2 = QLineEdit()
        v.addWidget(self.text1)
        v.addWidget(self.text2)
        self.button1 = QPushButton('确认')
        self.button1.pressed.connect(self.show_observation)
        self.label1 = QLabel('通视')
        v.addWidget(self.button1)
        v.addWidget(self.label1)
        l2 = QLabel('遮蔽度判断')
        self.text3 = QLineEdit()
        self.button2 = QPushButton('确认')
        self.button2.pressed.connect(self.show_info)
        self.label2 = QLabel('城镇')
        v.addWidget(l2)
        v.addWidget(self.text3)
        v.addWidget(self.button2)
        v.addWidget(self.label2)
        l3 = QLabel('高程分析')
        self.text4 = QLineEdit()
        self.button3 = QPushButton('确认')
        self.button3.pressed.connect(self.show_grid)
        self.label3 = QLabel('110')
        v.addWidget(l3)
        v.addWidget(self.text4)
        v.addWidget(self.button3)
        v.addWidget(self.label3)
        self.tab3.setLayout(v)
        l.addWidget(self.game_map)
        l.addWidget(self.t)
        l.setStretch(0, 2)
        l.setStretch(1, 1)
        self.setLayout(l)
    def show_red_message(self):
        try:
            name_1 = self.game_map.r1.name
            name_2 = self.game_map.r2.name
            position_1 = pos_to_hex_pos(self.game_map.r1.pos().x(), self.game_map.r1.pos().y())
            position_2 = pos_to_hex_pos(self.game_map.r2.pos().x(), self.game_map.r2.pos().y())
            d1 = get_distance(position_1, self.game_map.c1.hex_pos)
            d2 = get_distance(position_2, self.game_map.c1.hex_pos)
            d3 = get_distance(position_1, self.game_map.b1.hex_pos)
            d4 = get_distance(position_1, self.game_map.b2.hex_pos)
            d5 = get_distance(position_2, self.game_map.b1.hex_pos)
            d6 = get_distance(position_2, self.game_map.b2.hex_pos)
            self.r_p1.setPlainText(
                '算子1：{0} 位置：{1} 状态：机动 \n 距离夺控点：{2} \n 距离敌方算子距离：{3} {4} 可否射击： 否 否 \n\n 算子2：{5} 位置：{6} 状态：机动 \n 距离夺控点：{7} \n 距离敌方算子距离：{8} {9} 可否射击： 否 否'.format(name_1, position_1, d1, d3,d4, name_2, position_2, d2, d5,d6))
            t = self.r_p1.toPlainText()
            self.r_p5.setPlainText(t)
        except:
            self.r_p1.setPlainText('计算中...')
            self.r_p5.setPlainText('计算中...')
    def show_blue_message(self):
        try:
            name_1 = self.game_map.b1.name
            name_2 = self.game_map.b2.name
            position_1 = pos_to_hex_pos(self.game_map.b1.pos().x(), self.game_map.b1.pos().y())
            position_2 = pos_to_hex_pos(self.game_map.b2.pos().x(), self.game_map.b2.pos().y())
            d1 = get_distance(position_1, self.game_map.c1.hex_pos)
            d2 = get_distance(position_2, self.game_map.c1.hex_pos)
            d3 = get_distance(position_1, self.game_map.r1.hex_pos)
            d4 = get_distance(position_1, self.game_map.r2.hex_pos)
            d5 = get_distance(position_2, self.game_map.r1.hex_pos)
            d6 = get_distance(position_2, self.game_map.r2.hex_pos)
            self.r_p2.setPlainText(
                '算子1：{0} 位置：{1} 状态：机动 \n 距离夺控点：{2} \n 距离敌方算子距离：{3} {4} 可否射击： 否 否 \n\n 算子2：{5} 位置：{6} 状态：机动 \n 距离夺控点：{7} \n 距离敌方算子距离：{8} {9} 可否射击： 否 否'.format(name_1, position_1, d1, d3,d4, name_2, position_2, d2, d5,d6))
            t = self.r_p2.toPlainText()
            self.r_p4.setPlainText(t)
        except:
            self.r_p1.setPlainText('计算中...')
            self.r_p4.setPlainText('计算中...')
    def show_battle_suggest(self):
        try:
            self.r_p3.setPlainText('距离敌方远 \n 距离夺控点远 \n  首要目标：夺控 \n 建议红方坦克向右方夺控点机动')
            self.r_p6.setPlainText('距离敌方远 \n 距离夺控点远 \n  首要目标：夺控 \n 建议蓝方坦克向左方夺控点机动')
        except:
            self.r_p3.setPlainText('分析中……')
            self.r_p6.setPlainText('分析中……')
    def show_observation(self):
        try:
            hex1 = self.text1.text()
            hex2 = self.text2.text()
            value = check_observation(hex1, hex2, self.game_map.hexes)
            self.label1.setText(value)
        except:
            self.label1.setText('输入错误')
    def show_info(self):
        try:
            hex = self.text3.text()
            value = self.game_map.hexes[hex].cond
            if value == 7:
                self.label2.setText('城镇')
            else:
                self.label2.setText(str(value))
        except:
            self.label2.setText('输入错误')
    def show_grid(self):
        try:
            hex = self.text4.text()
            value = self.game_map.hexes[hex].ground_id
            self.label3.setText(str(value))
        except:
            self.label3.setText('输入错误')
