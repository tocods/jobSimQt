from PySide6.QtWidgets import (QGraphicsView, QVBoxLayout, QWidget, QGraphicsItem, QGraphicsScene, QGraphicsItemGroup,  QGraphicsPixmapItem, QGraphicsItemGroup, QGraphicsSimpleTextItem, QTreeWidget)
from qdarktheme.qtpy.QtGui import QPixmap, QFont, QColor
from qdarktheme.qtpy.QtCore import Qt, QSize, QPointF, QRectF
from item import GraphicItem, HostGraphicItem, SwitchGraphicItem
from edge import Edge
import globaldata

class MasterGraphicItem(QGraphicsItemGroup):

    def __init__(self, name, para, width=100, height=100, parent=None, view=None):  # para通常是图像名称
        super().__init__()
        self.para = para
        self.width = width
        self.height = height
        self.parent = parent
        self.view = view
        # 创建 QGraphicsPixmapItem 
        self.pixmap = QPixmap(para)
        self.pix = self.pixmap.scaled(QSize(self.width, self.height))
        self.pixmap_item = QGraphicsPixmapItem()
        self.pixmap_item.setPixmap(self.pix)
        self.addToGroup(self.pixmap_item)
        self.name = name
        self.text_item = QGraphicsSimpleTextItem(name)
        font = QFont("Arial", 12)
        self.text_item.setFont(font)

        # 获取图片和文本的宽度
        pixmap_width = self.pixmap_item.pixmap().width()
        text_width = self.text_item.boundingRect().width()

        # 设置文本位置，使其居中显示在图片下方
        text_pos = QPointF((pixmap_width - text_width) / 2, self.pixmap_item.pixmap().height() + 5)
        self.text_item.setPos(text_pos)

        # 将文本项添加到组中
        self.addToGroup(self.text_item)
        
        # 设置图元可以被选择或移动
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.view.graphicItemClicked(self, event)
        
        

class MasterScene(QGraphicsScene):
    def __init__(self, parent=None, view=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 500, 500)
        self.parentView = parent
        self.masterView = view
        self.nodes = []
        self.edges = []

    def setTreeWidget(self, treeWidget):
        self.treeWidget = treeWidget

    def printNet(self, software2Change=None):
        for node in self.parentView.gr_scene.nodes:
            if isinstance(node, HostGraphicItem):
                no = MasterGraphicItem(node.hostAttr.name, node.para, node.width, node.height, self, self.masterView)
            elif isinstance(node, SwitchGraphicItem):
                no = MasterGraphicItem(node.switchAttr.name, node.para, node.width, node.height, self, self.masterView)
            no.setPos(node.pos())
            self.addItem(no)
            self.nodes.append(no)
        if software2Change is not None:
            hostRemove = {}
            hostAdd = {}
            for i in range(len(software2Change)):
                originHost = software2Change[i][1]
                newHost = software2Change[i][2]
                software = software2Change[i][0]
                if originHost not in hostRemove:
                    hostRemove[originHost] = software
                else:
                    hostRemove[originHost] = hostRemove[originHost] + " " + software
                if newHost not in hostAdd:
                    hostAdd[newHost] = software
                else:
                    hostAdd[newHost] = hostAdd[newHost] + " " + software
                for node in self.nodes:
                    if node.name == originHost:
                        rect = QRectF()
                        rect.setX(float(node.pos().x()))
                        rect.setY(float(node.pos().y()))
                        rect.setWidth(100)
                        rect.setHeight(100)
                        c = QColor(Qt.red)
                        self.addRect(rect, c)
                    if node.name == newHost:
                        rect = QRectF()
                        rect.setX(float(node.pos().x()))
                        rect.setY(float(node.pos().y()))
                        rect.setWidth(100)
                        rect.setHeight(100)
                        c = QColor(Qt.green)
                        self.addRect(rect, c)
            for node in self.nodes:
                if node.name in hostRemove:
                    node.text_item.setText(node.name + "\n 移出软件：" + str(hostRemove[node.name]))
                if node.name in hostAdd:
                    node.text_item.setText(node.text_item.text() + "\n 加入软件：" + str(hostAdd[node.name]))