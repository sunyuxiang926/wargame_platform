import sys,os
from PyQt5.QtWidgets import QSizePolicy,QGridLayout,QDialog,QLabel,QApplication,QWidget,QTabWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QDialog, QPushButton, QLabel,QWidget,QApplication
from PyQt5.QtGui import QPixmap,QIcon
class ShowCurrentResult(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('推演结果')
        self.setWindowIcon(QIcon('tank.png'))
        self.setStyleSheet('QPushButton{color:black;background-color:white;border-radius:15px;border: 3px solid blue}')
        b1 = QPushButton(' 推演数据 ')
        b2 = QPushButton('返回')
        b1.pressed.connect(self.open_excel)
        b2.pressed.connect(self.close)
        v = QVBoxLayout()
        v.addWidget(b1)
        v.addWidget(b2)
        img_1 = QLabel()
        img_1.setMaximumSize(400, 400)
        img_1.setPixmap(QPixmap("get_goal_score.jpg"))
        img_1.setScaledContents(True)
        img_2 = QLabel()
        img_2.setMaximumSize(400, 400)
        img_2.setPixmap(QPixmap("kill_score.jpg"))
        img_2.setScaledContents(True)
        img_3 = QLabel()
        img_3.setMaximumSize(400, 400)
        img_3.setPixmap(QPixmap("survive_score.jpg"))
        img_3.setScaledContents(True)
        img_4 = QLabel()
        img_4.setMaximumSize(400, 400)
        img_4.setPixmap(QPixmap("win_rate.jpg"))
        img_4.setScaledContents(True)
        img_5 = QLabel()
        img_5.setMaximumSize(400, 400)
        img_5.setPixmap(QPixmap("win_times.jpg"))
        img_5.setScaledContents(True)
        img_6 = QLabel()
        img_6.setMaximumSize(400, 400)
        img_6.setPixmap(QPixmap("win_times.jpg"))
        img_6.setScaledContents(True)
        g = QGridLayout()
        g.addWidget(img_1,0,0)
        g.addWidget(img_2,0,1)
        g.addWidget(img_3,1,0)
        g.addWidget(img_4,1,1)
        g.addWidget(img_5,0,2)
        g.addWidget(img_6,1,2)
        h = QHBoxLayout()
        h.addLayout(v)
        h.addLayout(g)
        self.setLayout(h)
    def open_excel(self):
        import os
        os.system('测试2.xlsx')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = ShowCurrentResult()
    d.show()
    sys.exit(app.exec())
