# from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt
from qdarktheme.qtpy.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QGraphicsItemGroup, QGraphicsSimpleTextItem
from qdarktheme.qtpy.QtGui import QPixmap, QFont
from qdarktheme.qtpy.QtCore import Qt, QSize, QPointF
from entity.host import Host
from entity.switch import Switch
import globaldata


class GraphicItem(QGraphicsItemGroup):

    def __init__(self, name, para, width=100, height=100, parent=None):  # para通常是图像名称
        super().__init__()
        self.para = para
        self.width = width
        self.height = height
        self.parent = parent
        # 创建 QGraphicsPixmapItem 
        self.pixmap = QPixmap(para)
        self.pix = self.pixmap.scaled(QSize(self.width, self.height))
        self.pixmap_item = QGraphicsPixmapItem()
        self.pixmap_item.setPixmap(self.pix)
        self.addToGroup(self.pixmap_item)

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
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    # override
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_N:
            print("receive key_n\n")
        #     item = GraphicItem()
        #     item.setPos(0, 0)
        #     self.gr_scene.addItem(item)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # 如果图元被选中，就更新连线，这里更新的是所有。可以优化，只更新连接在图元上的。
        if self.isSelected():
            for gr_edge in self.scene().edges:
                gr_edge.edge_wrap.update_positions()

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self.parent.graphicItemClicked(self, event)

    def remove_from_globaldata(self):
        return

    def setName(self, name):
        self.text_item.setText(name)
        font = QFont("Arial", 12)
        self.text_item.setFont(font)

        # 获取图片和文本的宽度
        pixmap_width = self.pixmap_item.pixmap().width()
        text_width = self.text_item.boundingRect().width()

        # 设置文本位置，使其居中显示在图片下方
        text_pos = QPointF((pixmap_width - text_width) / 2, self.pixmap_item.pixmap().height() + 5)
        self.text_item.setPos(text_pos)
        self.update()

    


class HostGraphicItem(GraphicItem):
    def __init__(
        self,
        host_name,
        host_type,
        para,
        width=100,
        height=100,
        parent=None,
        Host_class=Host,
    ):
        super().__init__(host_name, para, width, height, parent=parent)
        # 主机属性
        # self.hostAttr = Host_class(host_name, host_type)
        # 使用给定的主机类存储数据
        self.hostAttr = Host_class(host_name)
        # 添加到全局变量中
        globaldata.hostList.append(self)

    def get_attr(self):
        return self.hostAttr

    def remove_from_globaldata(self):
        print(globaldata.linkList)
        i = 0
        while i < len(globaldata.linkList):
            if globaldata.linkList[i].start_item == self or globaldata.linkList[i].end_item == self:
                globaldata.linkList.pop(i)
            else:
                i += 1
        print(self)
        globaldata.hostList.remove(self)
        print(globaldata.hostList)



class SwitchGraphicItem(GraphicItem):
    def __init__(
        self,
        switch_name,
        switch_type,
        para,
        width=100,
        height=100,
        parent=None,
        Switch_class=Switch,
    ):
        super().__init__(switch_name, para, width, height, parent=parent)
        # 交换机属性
        # self.switchAttr = Switch_class(switch_name, switch_type)
        # 使用给定的交换机类存储数据
        self.switchAttr = Switch_class(switch_name)
        # 添加到全局变量中
        globaldata.switchList.append(self)

    def get_attr(self):
        return self.switchAttr

    def remove_from_globaldata(self):
        i = 0
        while i < len(globaldata.linkList):
            if globaldata.linkList[i].start_item == self or globaldata.linkList[i].end_item == self:
                globaldata.linkList.pop(i)
            else:
                i += 1
        globaldata.switchList.remove(self)
