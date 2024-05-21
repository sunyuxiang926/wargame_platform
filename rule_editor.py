import sys,os
from PyQt5.QtWidgets import QTreeWidgetItem,QTreeWidget,QHBoxLayout,QVBoxLayout,QDialog,QPushButton,QLabel,QWidget,QApplication,QTabWidget,QComboBox,QLineEdit
from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon
class UiWidget(QWidget):
    """
    规则编辑模块UI界面初始化设置与可视化
    """
    def __init__(self):
        super().__init__()
        h = QHBoxLayout()
        self.setLayout(h)
        w1 = QWidget()
        w2 = QWidget()
        w3 = QWidget()
        h.addWidget(w1)
        h.addWidget(w2)
        h.addWidget(w3)
        h.setStretch(0,1)
        h.setStretch(1, 1)
        h.setStretch(2, 1)
        v = QVBoxLayout()
        v2 = QVBoxLayout()
        v3 = QVBoxLayout()
        w1.setLayout(v)
        w2.setLayout(v2)
        w3.setLayout(v3)
        # 创建相关文本框
        l1 = QLabel('战场环境')
        l1.setAlignment(Qt.AlignCenter)
        l2 = QLabel('我方条件')
        l2.setAlignment(Qt.AlignCenter)
        l3 = QLabel('敌方条件')
        l3.setAlignment(Qt.AlignCenter)
        l4 = QLabel('夺控任务')
        l4.setAlignment(Qt.AlignCenter)
        l_11 = QLabel('地理环境')
        l_12= QLabel('气候环境')
        l_13 = QLabel('天气')
        l_14= QLabel('电磁干扰')
        self.g_env= QComboBox()
        self.g_env.addItems(['高原','平地','山地','滩涂','冰川','盆地','沙漠'])
        self.c_env = QComboBox()
        self.c_env.addItems(['热带季风','亚热带季风','温带季风','高原山地','温带大陆性','热带雨林'])
        self.w_env = QComboBox()
        self.w_env.addItems(['晴天','雨天','雪天','雾天'])
        self.e_env = QComboBox()
        self.e_env.addItems(['低','中','高'])
        tree = QTreeWidget()
        tree.setHeaderLabel('任务分解行动序列')
        root = QTreeWidgetItem(tree)
        root.setText(0,'回合阶段')
        child_1 = QTreeWidgetItem(root)
        child_1.setText(0,'展开部署')
        child_11 = QTreeWidgetItem(child_1)
        child_11.setText(0,'上车')
        child_12 = QTreeWidgetItem(child_1)
        child_12.setText(0, '编队')
        child_13 = QTreeWidgetItem(child_1)
        child_13.setText(0, '机动')
        child_2 = QTreeWidgetItem()
        child_2.setText(0,'机动侦察')
        child_21 = QTreeWidgetItem(child_2)
        child_21.setText(0,'机动')
        child_22 = QTreeWidgetItem(child_2)
        child_22.setText(0, '隐蔽')
        child_23 = QTreeWidgetItem(child_2)
        child_23.setText(0, '侦察')
        child_3 = QTreeWidgetItem(root)
        child_3.setText(0,'接敌交战')
        child_31 = QTreeWidgetItem(child_3)
        child_31.setText(0,'机动')
        child_32 = QTreeWidgetItem(child_3)
        child_32.setText(0, '直瞄')
        child_33 = QTreeWidgetItem(child_3)
        child_33.setText(0, '间瞄')
        child_4 = QTreeWidgetItem(root)
        child_4.setText(0,'冲锋夺占')
        child_41 = QTreeWidgetItem(child_4)
        child_41.setText(0,'机动')
        child_42 = QTreeWidgetItem(child_4)
        child_42.setText(0, '直瞄')
        child_43 = QTreeWidgetItem(child_4)
        child_43.setText(0, '近战')
        child_44 = QTreeWidgetItem(child_4)
        child_44.setText(0, '夺占')
        root.addChild(child_1)
        root.addChild(child_2)
        root.addChild(child_3)
        root.addChild(child_4)
        v.addWidget(tree)
        v.addWidget(l1)
        v.addWidget(l_11)
        v.addWidget(self.g_env)
        v.addWidget(l_12)
        v.addWidget(self.c_env)
        v.addWidget(l_13)
        v.addWidget(self.w_env)
        v.addWidget(l_14)
        v.addWidget(self.e_env)
        v.addWidget(l4)
        l_21 = QLabel('算子名称')
        l_22 = QLabel('算子类型')
        l_23 = QLabel('算子状态')
        l_24 = QLabel('兵力值')
        l_25 = QLabel('机动力')
        l_26 = QLabel('地形')
        l_27 = QLabel('弹药量')
        self.m_p= QComboBox()
        self.m_p.addItems(['步兵分队','装甲兵分队','坦克分队','重型战车分队','轻型突击车分队','无人机分队','武装直升机分队'])
        self.m_s= QComboBox()
        self.m_s.addItem('合成')
        self.m_z = QComboBox()
        self.m_z.addItems(['机动','隐蔽','驻止','压制'])
        self.m_c =QComboBox()
        self.m_c.addItems(['无','高','中','低'])
        self.m_m = QComboBox()
        self.m_m.addItems(['高','中','低','无'])
        self.m_g = QComboBox()
        self.m_g.addItems(['一般','居民地','树林','灌木','道路','铁路','桥梁','湿地','村庄','雪地'])
        self.m_w= QComboBox()
        self.m_w.addItems(['中','低','无','高'])
        v2.addWidget(l2)
        v2.addWidget(l_21)
        v2.addWidget(self.m_p)
        v2.addWidget(l_22)
        v2.addWidget(self.m_s)
        v2.addWidget(l_23)
        v2.addWidget(self.m_z)
        v2.addWidget(l_24)
        v2.addWidget(self.m_c)
        v2.addWidget(l_25)
        v2.addWidget(self.m_m)
        v2.addWidget(l_26)
        v2.addWidget(self.m_g)
        v2.addWidget(l_27)
        v2.addWidget(self.m_w)
        l_31 = QLabel('类型')
        l_32 = QLabel('地形')
        l_33 = QLabel('距离')
        l_34 = QLabel('位置')
        l_35 = QLabel('兵力值')
        l_36 = QLabel('特征')
        l_37 = QLabel('幅员')
        l_38 = QLabel('状态')
        self.e_s= QComboBox()
        self.e_s.addItems(['坐标','坦克分队','重型战车分队','轻型突击车分队','无人机分队','武装直升机分队','步兵分队','装甲兵分队'])
        self.e_g= QComboBox()
        self.e_g.addItems(['雪地','一般','居民地','树林','灌木','道路','铁路','桥梁','湿地','村庄'])
        self.e_d= QComboBox()
        self.e_d.addItems(['远','中','近'])
        self.e_l= QComboBox()
        self.e_l.addItems(['低','相同','高'])
        self.e_v= QComboBox()
        self.e_v.addItems(['低','高','中','无'])
        self.e_c= QComboBox()
        self.e_c.addItems(['点状','线状','面状'])
        self.e_e= QComboBox()
        self.e_e.addItems(['0','20m','50m'])
        self.e_z= QComboBox()
        self.e_z.addItems(['无','机动','隐蔽','驻止','压制'])
        v3.addWidget(l3)
        v3.addWidget(l_31)
        v3.addWidget(self.e_s)
        v3.addWidget(l_32)
        v3.addWidget(self.e_g)
        v3.addWidget(l_33)
        v3.addWidget(self.e_d)
        v3.addWidget(l_34)
        v3.addWidget(self.e_l)
        v3.addWidget(l_35)
        v3.addWidget(self.e_v)
        v3.addWidget(l_36)
        v3.addWidget(self.e_c)
        v3.addWidget(l_37)
        v3.addWidget(self.e_e)
        v3.addWidget(l_38)
        v3.addWidget(self.e_z)
class ShowKnowledge(QDialog):
    """
    1.陈述性知识与过程性知识表加载
    2.陈述性知识与过程性知识自定义编辑与对应知识保存更新
    3.不同推演作战环境下，陈述性与过程性知识的输出指导推演策略的调整
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('知识编辑器')
        self.resize(2000, 1000)
        self.setWindowIcon(QIcon('tank.png'))
        self.setStyleSheet('QPushButton{color:black;background-color:white;border-radius:15px;border: 3px solid blue}')
        self.t = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.t.addTab(self.tab1, "陈述性知识")
        self.t.addTab(self.tab2, "过程性知识")
        h = QHBoxLayout()
        h.addWidget(self.t)
        t1 = UiWidget()
        b1 = QPushButton(' 确认 ')
        b1.pressed.connect(self.show_cszs)
        b4 = QLabel('执行任务')
        self.b2 = QLineEdit()
        b5 = QLabel('任务策略类型')
        self.b6 = QLineEdit()
        b3 = QPushButton('打开陈述性知识总表')
        b3.pressed.connect(self.open_cszs)
        w1 = QWidget()
        v1 = QVBoxLayout()
        h1 = QHBoxLayout()
        h1.addWidget(b1)
        h1.addWidget(b4)
        h1.addWidget(self.b2)
        h1.addWidget(b5)
        h1.addWidget(self.b6)
        h1.addWidget(b3)
        w1.setLayout(h1)
        v1.addWidget(t1)
        v1.addWidget(w1)
        self.tab1.setLayout(v1)
        t2 = UiWidget()
        v2 = QVBoxLayout()
        w2 = QWidget()
        h2 = QHBoxLayout()
        t2_l1 = QLabel('我方坐标')
        t2_l2 = QComboBox()
        t2_l2.addItems(['(17, {})'.format(str(x)) for x in range(32)])
        t2_l3 = QLabel('敌方坐标')
        t2_l4 = QComboBox()
        t2_l4.addItems(['(18, {})'.format(str(x)) for x in range(32)])
        t2_l5 = QPushButton(' 确认 ')
        t2_l5.pressed.connect(self.show_gczs)
        t2_l6 = QLabel('执行任务')
        self.t2_l7 = QLineEdit()
        t2_l7 = QLabel('路径')
        self.t2_l8 = QLineEdit()
        t2_l8 = QLabel('使用武器')
        self.t2_l9 = QLineEdit()
        self.t2_10 = QPushButton('打开过程性知识总表')
        self.t2_10.pressed.connect(self.open_gczs)
        w2.setLayout(h2)
        h2.addWidget(t2_l1)
        h2.addWidget(t2_l2)
        h2.addWidget(t2_l3)
        h2.addWidget(t2_l4)
        h2.addWidget(t2_l5)
        h2.addWidget(t2_l6)
        h2.addWidget(self.t2_l7)
        h2.addWidget(t2_l7)
        h2.addWidget(self.t2_l8)
        h2.addWidget(t2_l8)
        h2.addWidget(self.t2_l9)
        h2.addWidget(self.t2_10)
        v2.addWidget(t2)
        v2.addWidget(w2)
        self.tab2.setLayout(v2)
        self.setLayout(h)
    # 陈述性知识调整后显示函数
    def show_cszs(self):
        self.b2.setText('机动')
        self.b6.setText('一般')
    # 过程性知识调整后显示函数
    def show_gczs(self):
        self.t2_l7.setText('机动')
        self.t2_l8.setText('无')
        self.t2_l9.setText('无')
    # 陈述性知识加载函数
    def open_cszs(self):
        import os
        os.system('陈述性知识.xlsx')
    # 过程性知识加载函数
    def open_gczs(self):
        import os
        os.system('过程性知识.xlsx')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = ShowKnowledge()
    d.show()
    sys.exit(app.exec())