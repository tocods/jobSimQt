from Window.EditHostNetargsWindow import *
from Window.EditLinkArgsWindow import EditLinkArgsWindow
from Window.EditSwitchNetargsWindow import *
import globaldata
from Window.SetHostArgsWindow import SetHostArgsWindow
from qdarktheme.qtpy.QtWidgets import (
    QGraphicsView,
    QGraphicsLineItem,
    QGraphicsPathItem,
    QGraphicsItemGroup,
)
from qdarktheme.qtpy.QtCore import Qt, QRect
from qdarktheme.qtpy.QtGui import QPainter, QPen

from item import GraphicItem, HostGraphicItem, SwitchGraphicItem
from edge import Edge, GraphicEdge
from HostInfoForm import HostInfoForm
from jobSim import jobSim
from HostInfoForm import HostInfoForm
from jobSim import sysSim
from entity.host import *
from entity.switch import *


class GraphicView(QGraphicsView):

    def __init__(self, graphic_scene, parent=None):
        super().__init__(parent)
        self.jobSim = sysSim
        self.gr_scene = graphic_scene
        self.parent = parent
        # self.edge_enable = False # 用来记录目前是否可以画线条
        self.drag_start_item = None
        # 子界面
        self.setHostArgsWindow = SetHostArgsWindow(self, sysSim)  # 将自己作为parent传入
        self.editHostNetargsWindowNormal = EditHostNetargsWindowNormal(self)
        self.editHostNetargsWindowUdp = EditHostNetargsWindowUdp(self)
        self.editHostNetargsWindowTcp = EditHostNetargsWindowTcp(self)
        self.editHostNetargsWindowRdma = EditHostNetargsWindowRdma(self)
        self.editHostNetargsWindowTsn = EditHostNetargsWindowTsn(self)
        self.editHostNetargsWindowDds = EditHostNetargsWindowDds(self)

        self.editSwitchNetargsWindowUdp = EditSwitchNetargsWindowUdp(self)
        self.editSwitchNetargsWindowTsn = EditSwitchNetargsWindowTsn(self)
        self.editSwitchNetargsWindowDds = EditSwitchNetargsWindowDds(self)
        self.editLinkArgsWindow = EditLinkArgsWindow(self)
        self.hostInform = HostInfoForm(self.jobSim)
        self.init_ui()

        self.lineToolEnabled = False

    def init_ui(self):
        self.setScene(self.gr_scene)
        # 设置渲染属性
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing
            |
            # QPainter.RenderHint.HighQualityAntialiasing |
            QPainter.RenderHint.TextAntialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
            | QPainter.RenderHint.LosslessImageRendering
        )
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        # 设置水平和竖直方向的滚动条显示
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        # 设置拖拽模式
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    # 在画布上添加主机
    def createGraphicHostItem(
        self,
        host_name,
        host_type,
        img,
        width,
        height,
        onlyCpu=False,
        Host_class=Host,
    ):
        item = HostGraphicItem(
            host_name, host_type, img, width, height, Host_class=Host_class
        )
        # 将onlyCpu记录到属性中
        item.hostAttr.only_cpu = onlyCpu
        item.setPos(0, 0)
        self.jobSim.addHostItem(item, onlyCPU=onlyCpu)
        self.gr_scene.add_node(item)
        return item

    # 在画布上添加交换机
    def createGraphicSwitchItem(
        self,
        switch_name,
        switch_type,
        img,
        width,
        height,
        Switch_class=Switch,
    ):
        item = SwitchGraphicItem(
            switch_name, switch_type, img, width, height, Switch_class=Switch_class
        )
        item.setPos(0, 0)
        self.gr_scene.add_node(item)
        return item

    # 在画布上添加连接
    def createGraphicLink(self, endpoint1, endpoint2):
        new_edge = Edge(self.gr_scene, endpoint1, endpoint2)
        # 保存连接线
        new_edge.store()

        return new_edge

    def keyPressEvent(self, event):
        # 新建图元样例，可忽略
        if event.key() == Qt.Key.Key_N:
            event.ignore()  # 忽略默认行为
            self.createGraphicHostItem("Model.png")

        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        # 点击鼠标时更新“位置”和“鼠标所在图元”
        super().mousePressEvent(event)
        self.mouse_pos = event.pos()
        self.mouse_pos_item = self.get_item_at_pos(event)  # self.itemAt(self.mouse_pos)
        #  如果是右键鼠标，弹出配置页
        if event.button() == Qt.MouseButton.RightButton:
            # TODO：可判断更多类型的主机，引导至不同类型主机的配置界面
            # 主机
            print(self.mouse_pos_item)
            if isinstance(self.mouse_pos_item, HostGraphicItem):
                # self.edit_form = HostInfoForm(self.mouse_pos_item, self.jobSim)
                self.setHostArgsWindow.binGraphicsItem(self.mouse_pos_item)
                # 将 主机图形对象 和 其中包含的主机属性信息对象 传递至属性设置界面
                self.setHostArgsWindow.setHostGraphicItem(self.mouse_pos_item)
                self.setHostArgsWindow.show()
                return
            # 交换机
            elif isinstance(self.mouse_pos_item, SwitchGraphicItem):
                # 将 交换机图形对象 和 其中包含的交换机属性信息对象 传递至属性设置界面
                if isinstance(self.mouse_pos_item.switchAttr, TsnSwitch):
                    self.editSwitchNetargsWindowTsn.setSwitchGraphicItem(
                        self.mouse_pos_item
                    )
                    self.editSwitchNetargsWindowTsn.show()
                else:
                    self.editSwitchNetargsWindowUdp.setSwitchGraphicItem(
                        self.mouse_pos_item
                    )
                    self.editSwitchNetargsWindowUdp.show()
                return
            # 连接
            elif isinstance(self.mouse_pos_item, GraphicEdge):
                # 将 连接图形对象 和 其中包含的连接属性信息对象 传递至属性设置界面
                self.editLinkArgsWindow.setLinkGraphicItem(self.mouse_pos_item)
                self.editLinkArgsWindow.show()
                return
        elif self.lineToolEnabled:
            self.lineClick(event)

    # 当前鼠标所在图元
    def get_item_at_pos(self, event):
        """Return the object that clicked on."""
        pos = event.pos()
        # item = self.itemAt(pos)
        """ 鼠标所在的10*10内都是选中范围 """
        area = QRect(pos.x() - 5, pos.y() - 5, 10, 10)
        if len(self.items(area)) == 0:
            return None
        result = self.items(area)[0]
        # if result.type() == GraphicItem.type or result.type() == QGraphicsPathItem
        result = result if result.type() == GraphicItem.type or isinstance(result, QGraphicsPathItem) else result.parentItem()
        return result

    def get_items_at_rubber(self):
        """Get group select items."""
        area = self.rubberBandRect()
        return self.items(area)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def lineToolEnable(self):
        if not self.lineToolEnabled:
            self.lineToolEnabled = True
            self.parent.ui.add_line.setText("停止连线")
        else:
            self.lineToolEnabled = False
            self.parent.ui.add_line.setText("连线")

    def lineClick(self, event):
        item = self.get_item_at_pos(event)
        if isinstance(item, GraphicItem):
            # 是起点
            if self.drag_start_item == None:
                self.drag_start_item = item
            # 是终点
            else:
                # 终点图元不能是起点图元，即无环图
                if item is not self.drag_start_item:
                    # 检查是否已经存在一条线
                    existed = False
                    for link in globaldata.linkList:
                        if (
                            link.start_item == self.drag_start_item
                            and link.end_item == item
                            or link.end_item == self.drag_start_item
                            and link.start_item == item
                        ):
                            existed = True
                    if not existed:
                        new_edge = Edge(self.gr_scene, self.drag_start_item, item)
                        # 保存连接线
                        new_edge.store()
                        self.drag_start_item = None
                        # self.lineToolEnable()
                else:
                    self.drag_start_item = None

    def delete_node(self):
        # 删除键
        item = self.mouse_pos_item
        if isinstance(item, QGraphicsItemGroup):
            self.gr_scene.remove_node(item)
        if isinstance(item, QGraphicsPathItem):
            self.gr_scene.remove_edge(item)

    # def mouseReleaseEvent(self, event):
    #         super().mouseReleaseEvent(event)
