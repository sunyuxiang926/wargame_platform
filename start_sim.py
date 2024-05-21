import sys
from importlib import import_module
from wargaming import *
from PyQt5.QtGui import QIcon
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLabel,QVBoxLayout,QFileDialog,QDialog,QRadioButton,QComboBox,QSlider



class StartSim(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(600,800)
        self.setWindowTitle('设置推演环境')
        self.setWindowIcon(QIcon('tank.png'))
        self.setStyleSheet(
            'QPushButton{color:black;background-color:white;border-radius:15px;border: 3px solid blue}')
        r1 = QRadioButton('机机对抗')
        r1.setChecked(True)
        l1 = QLabel('红方')
        self.c1 = QComboBox()
        self.c1.addItems(['PPO','IFN M-PPO（攻守兼备）','IFN M-PPO（注重进攻）','IFN M-PPO（注重防守）','RN M-PPO（攻守兼备）','RN M-PPO（注重进攻）','RN M-PPO（注重防守）','先验知识','DQN','PK-DQN','RNM-DQN','IFNM-DQN'])
        b1 = QPushButton('自定义加载')
        l2 = QLabel('蓝方')
        b2 = QPushButton('自定义加载')
        r2 = QRadioButton('人机对抗')
        c2 = QComboBox()
        c2.addItems(['红方-人 vs 蓝方-计算机','红方-计算机 vs 蓝方-人'])
        b3 = QPushButton('加载计算机')
        r3 = QRadioButton('人人对抗')
        l3 = QLabel('推演回合')
        c3 = QComboBox()
        c3.addItems(['1分钟','2分钟','3分钟','4分钟','5分钟'])
        l4 = QLabel('仿真地幅')
        c4 = QComboBox()
        c4.addItems(['1x1平方公里','2x2平方公里','3x3平方公里','4x4平方公里','5x5平方公里'])
        l5 = QLabel('仿真倍速')
        c5 = QComboBox()
        c5.addItems(['1x','2x','3x','4x','5x','6x','7x','8x','9x','10x','11x','12x','13x','14x','15x','16x'])
        b4 = QPushButton('开始运行')

        v = QVBoxLayout()
        v.addWidget(r1)
        v.addWidget(l1)
        v.addWidget(self.c1)
        v.addWidget(b1)
        v.addWidget(l2)
        v.addWidget(b2)
        v.addWidget(r2)
        v.addWidget(c2)
        v.addWidget(b3)
        v.addWidget(r3)
        v.addWidget(l3)
        v.addWidget(c3)
        v.addWidget(l4)
        v.addWidget(c4)
        v.addWidget(l5)
        v.addWidget(c5)
        v.addWidget(b4)
        self.setLayout(v)


        b1.pressed.connect(self.choose_file_1)
        b2.pressed.connect(self.choose_file_2)
        b4.pressed.connect(self.wargame_run)

    def choose_file_1(self):
        file,ok = QFileDialog.getOpenFileName(self, "打开",'.',"python files (*.py)")
        self.l1.setText(file)
        self.f1 = file




    def choose_file_2(self):
        file,ok = QFileDialog.getOpenFileName(self, "打开",'.',"python files (*.py)")
        self.l2.setText(file)
        self.f2 = file


    def wargame_run(self):
        text = self.c1.currentText()
        import os
        if text == 'PPO':
            os.system('python run_ppo.py')
        elif text == 'IFN M-PPO（攻守兼备）':
            os.system('python run_mhs_ppo_balance.py')
        elif text == 'IFN M-PPO（注重进攻）':
            os.system('python run_mhs_ppo_pushing.py')
        elif text == 'IFN M-PPO（注重防守）':
            os.system('python run_mhs_ppo_defence.py')
        elif text == 'RN M-PPO（攻守兼备）':
            os.system('python run_ss1_ppo.py')
        elif text == 'RN M-PPO（注重进攻）':
            os.system('python run_ss1_ppo1.py')
        elif text == 'RN M-PPO（注重防守）':
            os.system('python run_ss1_ppo2.py')
        elif text =='先验知识':
            os.system('python ./先验知识/main.py')

        else:
            pass

        # QApplication.exec()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = StartSim()
    w.show()
    sys.exit(app.exec())