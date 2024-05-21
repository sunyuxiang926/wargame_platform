import sys
import sqlite3
import xlrd
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QLineEdit,QDialog,QLabel,QGraphicsItem,QSlider,QPushButton,QHBoxLayout,QVBoxLayout,QFileDialog,QApplication,QGraphicsTextItem,QGraphicsPixmapItem,QGraphicsPathItem,QGraphicsScene,QGraphicsView,QMainWindow,QMenuBar,QWidget,QAction
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
        # ground_color = elevation_to_color[ground_id]
        # brush = QBrush(ground_color)
        # self.setBrush(brush)

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

    def load_map(self,map_data):
        for i in range(map_data.nrows):
            d = map_data.cell_value
            try:
                h = Hextile(d(i,0),d(i,1),d(i,2),d(i,3),d(i,4),d(i,5),d(i,6),d(i,7),d(i,8),d(i,9))

                color = elevation_to_color[h.ground_color]
                h.paintcolor(color)
                self.scene.addItem(h)


            except Exception as e:
                print(e)


    def accept_signal(self):
        self.parentWidget().parentWidget().show_selected_information()

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



class MapEditor(QMainWindow):
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
        self.l5 = GridLabel()
        v.addWidget(self.l5)


        l6 = QLabel('特征')
        v.addWidget(l6)
        self.l7 = CondLabel()
        v.addWidget(self.l7)




    def show_selected_information(self):
        self.l2.setText('六角格坐标: {}'.format(self.game_map.selected_item.hex_str))
        self.l4.setText(str(self.game_map.selected_item.ground_id))
        cond = self.game_map.selected_item.cond
        p1 = QPixmap('./resources/graphics/Hex/Hex/cond{}.png'.format(str(cond)))
        self.l5.setPixmap(p1)
        grid_id = self.game_map.selected_item.grid_id
        p2 = QPixmap('./resources/graphics/Hex/Hex/{}.png'.format(str(grid_id)))
        self.l7.setPixmap(p2)


    def change_scale(self,v):
        former_scale = self.game_map.transform().m11()
        self.game_map.scale(v/10.0/former_scale,v/10.0/former_scale)


    def open_file(self):
        file,ok = QFileDialog.getOpenFileName(self, "打开",'.',"Excel files (*.xls)")
        data = xlrd.open_workbook(file)
        game_map_data = data.sheet_by_index(0)

        self.game_map.load_map(game_map_data)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    map_editor = MapEditor()
    map_editor.show()
    sys.exit(app.exec())