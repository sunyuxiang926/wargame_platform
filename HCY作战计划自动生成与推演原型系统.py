import sys
from PyQt5.QtWidgets import QDialog,QApplication,QPushButton,QVBoxLayout,QLabel,QHBoxLayout,QMainWindow
from PyQt5.Qt import QSizePolicy,QStyleFactory
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import Qt, QThread

from map_editor import MapEditor
from start_sim import StartSim
from piece_editor import PieceEditor
from game_replay import GameReplay
from rule_editor import ShowKnowledge
from scenario_editor import ScenarioEditor
from show_current_result import ShowCurrentResult
from show_result import ShowResult
from new_function import NewFunction

class Demo(QMainWindow):
    """
    1.设计主界面底图和相关控件创建
    2.将每个空间与实现对应功能的.py文件对应
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('HCY作战计划自动生成与推演原型系统')
        self.setWindowIcon(QIcon('tank.png'))
        self.setStyleSheet('QDialog{background-color:green;border:10px solid #014F84}')
        self.resize(600,800)
        # 初始化主界面设置和图像设置
        w = QLabel()
        w.setPixmap(QPixmap('./resources/graphics/cover.png'))
        w.button1 = QPushButton('',w)
        w.button1.setGeometry(250,400,200,172)
        w.button1.setStyleSheet('QPushButton{border-image: url(./resources/graphics/b1.png)}')
        w.button2 = QPushButton('',w)
        w.button2.setGeometry(425,300,200,172)
        w.button2.setStyleSheet('QPushButton{border-image: url(./resources/graphics/b2.png)}')
        w.button3 = QPushButton('',w)
        w.button3.setGeometry(425,500,200,172)
        w.button3.setStyleSheet('QPushButton{border-image: url(./resources/graphics/b3.png)}')
        w.button4 = QPushButton('',w)
        w.button4.setGeometry(600,400,200,172)
        w.button4.setStyleSheet('QPushButton{border-image: url(./resources/graphics/b4.png)}')
        w.button5 = QPushButton('',w)
        w.button5.setGeometry(775,300,200,172)
        w.button5.setStyleSheet('QPushButton{border-image: url(./resources/graphics/b5.png)}')
        w.button6 = QPushButton('',w)
        w.button6.setGeometry(775,500,200,172)
        w.button6.setStyleSheet('QPushButton{border-image: url(./resources/graphics/b6.png)}')
        w.button7 = QPushButton('',w)
        w.button7.setGeometry(950,400,200,172)
        w.button7.setStyleSheet('QPushButton{border-image: url(./resources/graphics/b7.png)}')

        w.button8 = QPushButton('', w)
        w.button8.setGeometry(600,200,200,172)
        w.button8.setStyleSheet('QPushButton{border-image: url(./resources/graphics/08.png)}')
        self.setCentralWidget(w)


        # 添加主界面控件链接对应.py文件
        w.button1.pressed.connect(self.map_edit)
        w.button2.pressed.connect(self.replay)
        w.button3.pressed.connect(self.rule_edit)
        w.button4.pressed.connect(self.scenario_edit)
        w.button5.pressed.connect(self.start_simulation)
        w.button6.pressed.connect(self.show_result)
        w.button7.pressed.connect(self.data_analysis)
        w.button8.pressed.connect(self.add_new_function)
    # 地图编辑功能控件设计与跳转函数
    def map_edit(self):
        map_editor = MapEditor()
        map_editor.exec()
    # 复盘分析功能控件设计与跳转函数
    def replay(self):
        game_replay = GameReplay()
        game_replay.exec()
    # 规则编辑功能控件设计与跳转函数
    def rule_edit(self):
        rule_editor = ShowKnowledge()
        rule_editor.exec()
    # 推演设置功能控件设计与跳转函数
    def scenario_edit(self):
        scenario_editor = ScenarioEditor()
        scenario_editor.exec()
    # 推演分析功能控件设计与跳转函数
    def show_result(self):
        result = ShowCurrentResult()
        result.exec()
    # 想定编辑功能控件设计与跳转函数
    def start_simulation(self):
        # pass
        s = StartSim()
        s.exec()
    # 推演分析功能控件设计与跳转函数
    def data_analysis(self):
        s = ShowResult()
        s.exec()

    def add_new_function(self):
        s = NewFunction()
        s.exec()
# 主界面使用主函数
if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    w = Demo()
    w.show()
    sys.exit(app.exec())