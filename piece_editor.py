import sys
import sqlite3
import xlrd
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QTextEdit,QSpinBox,\
    QLineEdit,QGridLayout,QComboBox,QApplication, QWidget, QPushButton,QLabel,QVBoxLayout,QFileDialog,QDialog,QRadioButton

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
sql = 'SELECT * FROM 算子编辑'
cursor.execute(sql)
data = cursor.fetchall()
conn.close()

class PieceEditor(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('算子编辑')
        v = QVBoxLayout()
        l = QLabel('选择算子')
        l.setAlignment(Qt.AlignCenter)
        v.addWidget(l)
        self.piece = QComboBox()
        self.piece.addItem('请选择...')
        self.piece.currentTextChanged.connect(self.show_information)
        for piece in data:
            self.piece.addItem(piece[0])
        v.addWidget(self.piece)
        gl = QGridLayout()
        gl.addWidget(QLabel('棋子类型'),0,0)
        gl.addWidget(QLabel('机动力值'),1,0)
        gl.addWidget(QLabel('装甲类型'),2,0)
        gl.addWidget(QLabel('分值'),3,0)
        self.t1 = QLineEdit('')
        gl.addWidget(self.t1,0,1)
        self.t2 = QSpinBox()
        self.t2.setMinimum(1)
        self.t2.setMaximum(20)
        gl.addWidget(self.t2,1,1)
        self.t3 = QComboBox()
        self.t3.addItem('复合装甲')
        self.t3.addItem('重型装甲')
        self.t3.addItem('中型装甲')
        self.t3.addItem('无装甲')
        gl.addWidget(self.t3,2,1)
        self.t4 = QLineEdit()
        gl.addWidget(self.t4,3,1)

        gl.addWidget(QLabel('观察距离（对人）'),0,2)
        gl.addWidget(QLabel('观察距离（对车）'), 1, 2)
        gl.addWidget(QLabel('行进间射击能力'), 2, 2)
        self.label = QLabel('车载导弹基数')
        gl.addWidget(self.label, 3, 2)

        self.t5 = QLineEdit()
        self.t6 = QLineEdit()
        self.t7 = QLineEdit()
        self.t8 = QLineEdit()

        gl.addWidget(self.t5, 0, 3)
        gl.addWidget(self.t6, 1, 3)
        gl.addWidget(self.t7, 2, 3)
        gl.addWidget(self.t8, 3, 3)
        self.text = QTextEdit()


        v.addLayout(gl)
        v.addWidget(self.text)
        self.button = QPushButton('确定')
        self.button.pressed.connect(self.close)
        v.addWidget(self.button)
        self.setLayout(v)

    def show_information(self,text):
        if text != '请选择...':
            for item in data:
                if text == item[0]:
                    self.t1.setText(item[1])
                    self.t2.setValue(item[2])
                    self.t3.setCurrentText(item[3])
                    self.t4.setText(str(item[4]))
                    self.t5.setText(str(item[5]))
                    self.t6.setText(str(item[6]))
                    self.t7.setText(item[7])
                    self.t8.setText(str(item[8]))
                    self.text.setText(item[10])




if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = PieceEditor()
    d.show()
    sys.exit(app.exec())