import sys
import sqlite3
import xlrd
from PyQt5.QtWidgets import QVBoxLayout,QTreeWidget,QTreeWidgetItem,QTableWidget,QTableWidgetItem,QLineEdit,QDialog,QLabel,QGraphicsItem,QSlider,QPushButton,QHBoxLayout,QVBoxLayout,QFileDialog,QApplication,QGraphicsTextItem,QGraphicsPixmapItem,QGraphicsPathItem,QGraphicsScene,QGraphicsView,QMainWindow,QMenuBar,QWidget,QAction
from PyQt5.QtGui import QColor,QBrush,QPainterPath,QPixmap,QPalette,QFont,QIcon
from PyQt5.Qt import Qt


conn = sqlite3.connect('test.db')
cursor = conn.cursor()




class ScenarioEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('想定编辑器')
        self.resize(2000, 1000)
        menu_file = self.menuBar().addMenu('文件')
        open_action = QAction('打开', self)
        menu_file.addAction(open_action)
        open_action.triggered.connect(self.open_file)

    def open_file(self):
        dia = QDialog()
        dia.resize(800,600)
        tree = QTreeWidget()
        tree.itemClicked.connect(self.choose_scenario)
        tree.menu = QTreeWidgetItem(tree)
        tree.setHeaderLabels(['想定目录'])
        tree.menu.setText(0, '地图名称')
        sql = 'SELECT 地图名称 FROM 地图目录'
        cursor.execute(sql)
        data = cursor.fetchall()
        item = {}
        for i in data:
            item[i[0]] = QTreeWidgetItem()
            item[i[0]].setText(0,i[0])
            tree.menu.addChild(item[i[0]])
        cursor.execute('SELECT 名称 FROM 城镇居民地想定目录')
        data = cursor.fetchall()
        for i in data:
            s = QTreeWidgetItem()
            s.setText(0,i[0])
            item['城镇居民地'].addChild(s)
        for i in range(4):
            s = QTreeWidgetItem()
            s.setText(0,'占位符')
            item['岛上台地'].addChild(s)
        for i in range(3):
            s = QTreeWidgetItem()
            s.setText(0,'占位符')
            item['高原通道'].addChild(s)
        v = QVBoxLayout()
        self.l = QLabel('城镇居民地_想定1')
        self.b = QPushButton('确定')
        self.b.pressed.connect(self.load)
        v.addWidget(tree)
        v.addWidget(self.l)
        v.addWidget(self.b)
        dia.setLayout(v)

        dia.exec()


    def choose_scenario(self,item,column):
        self.l.setText(item.text(column))

    def load(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = ScenarioEditor()
    editor.show()
    sys.exit(app.exec())

