# from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt
from qdarktheme.qtpy.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
from qdarktheme.qtpy.QtGui import QPixmap, QColor
from qdarktheme.qtpy.QtCore import Qt, QSize, QRectF
import globaldata
from util.jobSim import FlowNet

class GraphicItem(QGraphicsPixmapItem):

    def __init__(self, para, name, windows, width=100, height=100, parent=None): #para通常是图像名称
        super().__init__(parent)
        self.para = para
        self.pixmap = QPixmap(para)
        # print(self.pixmap)
        self.pix = self.pixmap.scaled(QSize(int(width), int(height)))
        self.width = width
        self.height = height
        self.name = name
        self.see = windows
        self.setPixmap(self.pix)    
        # 设置图元可以被选择或移动
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
    


    #override
    def keyPressEvent(self, event):
        print("111")
        self.see.__addPoint(self.name)
        # if event.key() == Qt.Key.Key_N:
        #     print("receive key_n\n")
            
        #     item = GraphicItem()
        #     item.setPos(0, 0)
        #     self.gr_scene.addItem(item)

    def mouseDoubleClickEvent(self, event):
        print("22")
        if self.see.lastChose == None:
            self.see.nowFlow = FlowNet()
            self.see.nowFlow.addNode(self.name)
            self.see.lastChose = self.name
            x = -1
            y = -1
            if self.name in self.see.netHosts:
                x = self.see.netHosts[self.name].x
                y = self.see.netHosts[self.name].y
            if self.name in self.see.netSwtichs:
                x = self.see.netSwtichs[self.name].x
                y = self.see.netSwtichs[self.name].y
            rect = QRectF()
          
            rect.setX(float(x))
            rect.setY(float(y))
            rect.setWidth(100)
            rect.setHeight(100)
            c = QColor(Qt.red)
            self.see.screne.addRect(rect, c)
            return
        ifHasLink = False
        for link in self.see.netLinks.values():
            if link.p1 == self.see.lastChose and link.p2 == self.name :
                ifHasLink = True
                break
            if link.p2 == self.see.lastChose and link.p1 == self.name :
                ifHasLink = True
                break
        if self.see.lastlastChose == self.name:
            ifHasLink = False
        if ifHasLink:
            x = -1
            y = -1
            if self.name in self.see.netHosts:
                x = self.see.netHosts[self.name].x
                y = self.see.netHosts[self.name].y
            if self.name in self.see.netSwtichs:
                x = self.see.netSwtichs[self.name].x
                y = self.see.netSwtichs[self.name].y
            rect = QRectF()
            self.see.nowFlow.addNode(self.name)
            rect.setX(float(x))
            rect.setY(float(y))
            rect.setWidth(100)
            rect.setHeight(100)
            c = QColor(Qt.red)
            self.see.screne.addRect(rect, c)
            self.see.lastlastChose = self.see.lastChose
            self.see.lastChose = self.name
        return super().mouseDoubleClickEvent(event)
        

    def remove_from_globaldata(self):
        return




class HostGraphicItem(GraphicItem):
    def __init__(self, host_name, host_type, para, width=100, height=100, parent=None):
        super().__init__(para, width, height, parent=None)
        self.type = "Host"
        # 主机属性
        # self.hostAttr = Host_class(host_name, host_type)
        # 使用给定的主机类存储数据

       

    def get_attr(self):
        return self.hostAttr
    
    def remove_from_globaldata(self):
        globaldata.hostList.remove(self)

class SwitchGraphicItem(GraphicItem):
    def __init__(self, switch_name, switch_type, para, width=100, height=100, parent=None):
        super().__init__(para, width, height, parent=None)
        self.type = "Switch"
      

    def get_attr(self):
        return self.switchAttr
    
    def remove_from_globaldata(self):
        globaldata.switchList.remove(self)