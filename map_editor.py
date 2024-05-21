import sys
import sqlite3
import xlrd
import xlwt
from PyQt5.QtWidgets import QStyle,QStyleOptionSlider,QMessageBox,QTableWidget,QTableWidgetItem,QLineEdit,QDialog,QLabel,QGraphicsItem,QSlider,QPushButton,QHBoxLayout,QVBoxLayout,QFileDialog,QApplication,QGraphicsTextItem,QGraphicsPixmapItem,QGraphicsPathItem,QGraphicsScene,QGraphicsView,QMainWindow,QMenuBar,QWidget,QAction
from PyQt5.QtGui import QColor,QBrush,QPainterPath,QPixmap,QPalette,QFont,QIcon
from PyQt5.Qt import Qt
import pymysql
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
class Slider(QSlider):
    def mousePressEvent(self, event):
        # 鼠标事件判断函数
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
        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin, sliderMax - sliderMin, opt.upsideDown)
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
        self.ground_color = ground_id
        QGraphicsPixmapItem(QPixmap('./resources/graphics/Hex/Hex/cond{}.png'.format(str(int(cond)))), self)
        self.cond = int(cond)
        QGraphicsPixmapItem(QPixmap('./resources/graphics/Hex/Hex/{}.png'.format(str(int(grid_id)))), self)
        self.grid_id = int(grid_id)
        self.map_id = int(map_id)
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
    def paintcolor(self,color):
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
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0,0,3000,3000)
        self.setScene(self.scene)
        self.selected_item = None
        self.hexes = {}
        self.data = None
    def load_map(self,map_data):
        for i in range(map_data.nrows):
            d = map_data.cell_value
            self.data = d
            try:
                h = Hextile(d(i,0),d(i,1),d(i,2),d(i,3),d(i,4),d(i,5),d(i,6),d(i,7),d(i,8),d(i,9))
                self.hexes[h.hex_str] = h

                color = elevation_to_color[h.ground_color]
                self.hexes[h.hex_str].paintcolor(color)
                self.scene.addItem(self.hexes[h.hex_str])
            except Exception as e:
                print(e)
    def accept_signal(self):
        self.parentWidget().show_selected_information()

class GridLabel(QLabel):
    def __init__(self):
        super().__init__()
    def mousePressEvent(self, QMouseEvent):
        d = QDialog()
        table = QTableWidget(d)
        table.setColumnCount(10)
        table.setRowCount(17)
        table.setGeometry(0,0,600,1000)
        for i in range(10):
            table.setColumnWidth(i,58)
        for i in range(1,171):
            item = QTableWidgetItem()
            p = QIcon('./resources/graphics/Hex/Hex/{}.png'.format(i))
            item.setIcon(p)
            j = (i-1)//10
            k = (i-1)%10
            table.setItem(j,k,item)
            item.num = i
        table.itemClicked.connect(self.change_image)
        d.exec()
    def change_image(self,item):
        p = QPixmap('./resources/graphics/Hex/Hex/{}.png'.format(str(item.num)))
        self.setPixmap(p)
        self.parentWidget().parentWidget().change_grid(item.num)


class CondLabel(QLabel):
    def __init__(self):
        super().__init__()
    def mousePressEvent(self, QMouseEvent):
        d = QDialog()
        table = QTableWidget(d)
        table.setColumnCount(7)
        table.setRowCount(1)
        table.setGeometry(0,0,500,200)
        for i in range(7):
            table.setColumnWidth(i,58)
        for i in range(1,8):
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            p = QIcon('./resources/graphics/Hex/Hex/cond{}.png'.format(i))
            item.setIcon(p)
            table.setItem(0,i-1,item)
            item.num = i
        table.itemClicked.connect(self.change_image)
        d.exec()
    def change_image(self,item):
        p = QPixmap('./resources/graphics/Hex/Hex/cond{}.png'.format(str(item.num)))
        self.setPixmap(p)
        self.parentWidget().parentWidget().change_cond(item.num)



class MapEditor(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('地图编辑器')
        self.setWindowIcon(QIcon('tank.png'))
        self.setStyleSheet(
            'QPushButton{color:black;background-color:white;border-radius:15px;border: 3px solid blue}')
        self.resize(2000,1000)
        l = QHBoxLayout()
        self.game_map = GameMap()
        self.control = QWidget()
        l.addWidget(self.game_map)
        l.addWidget(self.control)
        self.setLayout(l)
        v = QVBoxLayout()
        self.control.setLayout(v)
        # 添加打开控件，打开计算机文件资源管理器
        self.button = QPushButton('打开')
        self.button.setDefault(False)
        self.button.pressed.connect(self.open_file)
        # 添加尺寸调整滑动条进行地图尺寸的放缩
        v.addWidget(self.button)
        l1 = QLabel('尺寸调整')
        v.addWidget(l1)
        # 设置导入地图的初始大小、滑动条放缩的最大与最小范围；
        s = Slider(Qt.Horizontal)
        v.addWidget(s)
        s.setMinimum(6)
        s.setMaximum(20)
        s.setValue(10)
        s.setTickInterval(2)
        s.setSingleStep(2)
        s.setTickPosition(QSlider.TicksBelow)
        s.valueChanged.connect(self.change_scale)#添加滑动条点选滑动选择
        # 添加“六角格坐标”文本提示信息
        self.l2 = QLabel('六角格坐标: ')
        v.addWidget(self.l2)
        # 添加“高程”文本提示信息
        l3 = QLabel('高程')
        v.addWidget(l3)
        # 添加“六角格坐标”文本提示信息
        self.l4 = QLineEdit('')
        v.addWidget(self.l4)
        self.l_button = QPushButton('确定')
        self.l_button.pressed.connect(self.change_elavation)
        self.l_button.setDefault(True)
        v.addWidget(self.l_button)
        l4 = QLabel('地形')
        v.addWidget(l4)
        self.l5 = GridLabel()
        v.addWidget(self.l5)
        l6 = QLabel('特征')
        v.addWidget(l6)
        self.l7 = CondLabel()
        v.addWidget(self.l7)
        self.button_1 = QPushButton('保存')
        v.addWidget(self.button_1)
        self.button_1.pressed.connect(self.save_excel)
    def save_excel(self):
        workbook = xlwt.Workbook(encoding ='utf-8')
        booksheet = workbook.add_sheet('查询', cell_overwrite_ok=True)
        i = 1
        for key,value in self.game_map.hexes.items():
            booksheet.write(i,0,'83')
            booksheet.write(i,1,value.map_id)
            booksheet.write(i,2,value.hex_str)
            booksheet.write(i,3,0)
            booksheet.write(i, 4,0)
            booksheet.write(i, 5, value.cond)
            booksheet.write(i, 6, 0)
            booksheet.write(i, 7, value.grid_id)
            booksheet.write(i, 8, 0)
            booksheet.write(i, 9, value.ground_id)
            i += 1
        workbook.save(self.file)
        self.close()
    def close_dia(self):
        self.close()
    def change_elavation(self):
        try:
            a = int(self.l4.text())
            if a%10 == 0 and 100 <= a <= 150:
                item = self.game_map.selected_item
                new_item = Hextile(None,item.map_id,None,None,None,item.cond,None,item.grid_id,None,a)
                self.game_map.scene.removeItem(item)
                self.game_map.scene.addItem(new_item)
                self.game_map.hexes[item.hex_str] = new_item
                self.game_map.selected_item = new_item
                color = elevation_to_color[a]
                self.game_map.selected_item.paintcolor(color)
            else:
                QMessageBox.information(None, '提示', '请输入一个合理的高度', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        except:
            QMessageBox.information(None,'提示','请输入一个合适的高度',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
    def change_grid(self,num):
        try:
            item = self.game_map.selected_item
            new_item = Hextile(None, item.map_id, None, None, None, item.cond, None, num, None, item.ground_id)
            self.game_map.scene.removeItem(item)
            self.game_map.scene.addItem(new_item)
            self.game_map.hexes[item.hex_str] = new_item
            self.game_map.selected_item = new_item
            color = elevation_to_color[item.ground_id]
            self.game_map.selected_item.paintcolor(color)
        except:
            QMessageBox.information(None,'提示','非法操作',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
    def change_cond(self,num):
        try:
            item = self.game_map.selected_item
            new_item = Hextile(None, item.map_id, None, None, None, num, None, item.grid_id, None, item.ground_id)
            self.game_map.scene.removeItem(item)
            self.game_map.scene.addItem(new_item)
            self.game_map.hexes[item.hex_str] = new_item
            self.game_map.selected_item = new_item
            color = elevation_to_color[item.ground_id]
            self.game_map.selected_item.paintcolor(color)
        except:
            QMessageBox.information(None,'提示','非法操作',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
    def show_selected_information(self):
        self.l2.setText('六角格坐标: {}'.format(self.game_map.selected_item.hex_str))
        self.l4.setText(str(self.game_map.selected_item.ground_id))
        cond = self.game_map.selected_item.cond
        p1 = QPixmap('./resources/graphics/Hex/Hex/cond{}.png'.format(str(cond)))
        self.l7.setPixmap(p1)
        grid_id = self.game_map.selected_item.grid_id
        p2 = QPixmap('./resources/graphics/Hex/Hex/{}.png'.format(str(grid_id)))
        self.l5.setPixmap(p2)
    def change_scale(self,v):
        former_scale = self.game_map.transform().m11()
        self.game_map.scale(v/10.0/former_scale,v/10.0/former_scale)
    def open_file(self):
        self.file,ok = QFileDialog.getOpenFileName(self, "打开",'.',"Excel files (*.xls)")
        data = xlrd.open_workbook(self.file)
        print(self.file)
        game_map_data = data.sheet_by_index(0)
        self.game_map.load_map(game_map_data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    map_editor = MapEditor()
    map_editor.show()
    sys.exit(app.exec())