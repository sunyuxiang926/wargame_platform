from PyQt5.Qt import QFont
from PyQt5.QtWidgets import QGraphicsPathItem,QGraphicsItem,QGraphicsPixmapItem,QGraphicsTextItem,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QPainterPath,QBrush,QPixmap




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
        self.hexes ={}

    def load_map(self,map_data,map_color):
        for i in range(map_data.nrows):
            d = map_data.cell_value
            try:
                h = Hextile(d(i,0),d(i,1),d(i,2),d(i,3),d(i,4),d(i,5),d(i,6),d(i,7),d(i,8),d(i,9))
                self.hexes[h.hex_str] = h
                h.paintcolor(map_color(h.ground_color))
                self.scene.addItem(h)
            except Exception as e:
                print(e)


    def accept_signal(self):
        self.parentWidget().parentWidget().show_selected_information()