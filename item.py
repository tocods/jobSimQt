# from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt
from qdarktheme.qtpy.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
from qdarktheme.qtpy.QtGui import QPixmap
from qdarktheme.qtpy.QtCore import Qt, QSize
from entity.host import Host
from entity.switch import Switch
import globaldata


class GraphicItem(QGraphicsPixmapItem):

    def __init__(self, para, width=100, height=100, parent=None):  # para通常是图像名称
        super().__init__(parent)
        self.para = para
        self.pixmap = QPixmap(para)
        # print(self.pixmap)
        self.pix = self.pixmap.scaled(QSize(int(width), int(height)))
        self.width = width
        self.height = height
        self.setPixmap(self.pix)
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

    def remove_from_globaldata(self):
        return


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
        super().__init__(para, width, height, parent=None)
        # 主机属性
        # self.hostAttr = Host_class(host_name, host_type)
        # 使用给定的主机类存储数据
        self.hostAttr = Host_class(host_name)
        # 添加到全局变量中
        globaldata.hostList.append(self)

    def get_attr(self):
        return self.hostAttr

    def remove_from_globaldata(self):
        print("remove_from_globaldata")
        print(globaldata.linkList)
        i = 0
        while i < len(globaldata.linkList):
            if globaldata.linkList[i].start_item == self or globaldata.linkList[i].end_item == self:
                globaldata.linkList.pop(i)
            else:
                i += 1
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
        super().__init__(para, width, height, parent=None)
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
