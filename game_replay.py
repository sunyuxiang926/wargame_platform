import sys
import sqlite3
import xlrd
import random
from PyQt5.QtWidgets import QStyle,QStyleOptionSlider,QPlainTextEdit, QComboBox, QTabWidget, QTableWidgetItem, QLineEdit, QDialog, QLabel, \
    QGraphicsItem, QSlider, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QApplication, QGraphicsTextItem, \
    QGraphicsPixmapItem, QGraphicsPathItem, QGraphicsScene, QGraphicsView, QMainWindow, QMenuBar, QWidget, QAction
from PyQt5.QtGui import QColor, QBrush, QPainterPath, QPixmap, QPalette, QFont, QIcon
from PyQt5.QtCore import QObject, pyqtSignal,QTimer
from PyQt5.Qt import Qt
class Slider(QSlider):
    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)

    def pixelPosToRangeValue(self, pos):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)

        if self.orientation() == Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1;
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()
        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                               sliderMax - sliderMin, opt.upsideDown)
# 计算两点之间位置关系，判断是否通视
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
# 计算算子间距离
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
# 通视判断函数
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
    """
    夺控点设置与夺控点图标可视化
    """
    def __init__(self, name, hex_pos):
        super().__init__(name, hex_pos)
        self.setPixmap(QPixmap('./resources/graphics/qtimg/Control points.png'))
class RTank(Piece):
    """
    红方坦克算子可视化
    """
    def __init__(self, name, hex_pos):
        super().__init__(name, hex_pos)
        p = QPixmap('./resources/graphics/qtimg/UNITs1_26.jpg')
        self.setPixmap(p)
class BTank(Piece):
    """
    蓝方坦克算子可视化
    """
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
    """
    推演地图初始、推演地图加载
    """
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 3000, 3000)
        self.setScene(self.scene)
        self.selected_item = None
        self.hexes = {}
        self.data = None
        self.speed = 1000
    def load_map(self):
        import xlrd
        data = xlrd.open_workbook('./resources/game_maps/01 城镇居民地.xls')
        game_map_data = data.sheet_by_index(0)
        self.e = MyObject()
        for i in range(game_map_data.nrows):
            d = game_map_data.cell_value
            self.data = d
            try:
                h = Hextile(d(i, 0), d(i, 1), d(i, 2), d(i, 3), d(i, 4), d(i, 5), d(i, 6), d(i, 7), d(i, 8), d(i, 9))
                self.hexes[h.hex_str] = h
                self.scene.addItem(self.hexes[h.hex_str])
            except Exception as e:
                print(e)
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
class GameReplay(QDialog):
    """
    推演过程回放相关函数
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('复盘分析')
        self.resize(2000, 1000)
        self.setWindowIcon(QIcon('tank.png'))
        self.setStyleSheet(
            'QPushButton{color:black;background-color:white;border-radius:15px;border: 3px solid blue}')
        self.num = 0
        self.order_1 =[]
        self.order_2 =[]
        with open('test.txt', 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                o1 = line[:16]
                o2 = line[17:]
                self.order_1.append(o1)
                self.order_2.append(o2)
        self.timer = QTimer()
        self.timer.stop()
        self.timer.timeout.connect(self.update)
        l = QHBoxLayout()
        self.game_map = GameMap()
        w = QWidget()
        v = QVBoxLayout()
        w.setLayout(v)
        b = QPushButton('打开')
        b.pressed.connect(self.open_file)
        v.addWidget(b)
        l1 = QLabel('尺寸调整')
        v.addWidget(l1)
        s = Slider(Qt.Horizontal)
        v.addWidget(s)
        s.setMinimum(6)
        s.setMaximum(20)
        s.setValue(10)
        s.setTickInterval(2)
        s.setTickPosition(QSlider.TicksBelow)
        s.valueChanged.connect(self.change_scale)
        # 推演速度调整
        l2 = QLabel('速度调整(需先暂停)')
        v.addWidget(l2)
        s2 = Slider(Qt.Horizontal)
        v.addWidget(s2)
        s2.setMinimum(2)
        s2.setMaximum(16)
        s2.setValue(8)
        s2.setTickInterval(2)
        s2.setTickPosition(QSlider.TicksBelow)
        s2.valueChanged.connect(self.change_speed)
        # 推演过程暂停与继续
        b2 = QPushButton('暂停/继续')
        b2.pressed.connect(self.pause)
        v.addWidget(b2)
        self.b3 = QPlainTextEdit()
        v.addWidget(self.b3)
        l.addWidget(self.game_map)
        l.addWidget(w)
        l.setStretch(0,3)
        l.setStretch(1,1)
        self.setLayout(l)
    # 推演回放过程暂停函数
    def pause(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(self.game_map.speed)
    # 推演回放速度调整函数
    def change_speed(self,v):
        self.game_map.speed = 1800 - v*100
    # 推演回放地图尺寸调整函数
    def change_scale(self,v):
        former_scale = self.game_map.transform().m11()
        self.game_map.scale(v/10.0/former_scale,v/10.0/former_scale)
    # 推演回放文件加载函数
    def open_file(self):
        file,ok = QFileDialog.getOpenFileName(self, "打开",'.')
        self.game_map.load_map()
    # 推演回放干预信息更新函数
    def update(self):
        if self.num < len(self.order_2):
            order = self.order_2[self.num]
            eval(order)
            self.game_map.viewport().update()
            self.b3.setPlainText(self.order_1[self.num])
            self.num +=1
        else:
            pass




if __name__ == '__main__':
    app = QApplication(sys.argv)
    map_editor = GameReplay()
    map_editor.show()
    sys.exit(app.exec())



