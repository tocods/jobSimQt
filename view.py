from qdarktheme.qtpy.QtGui import QMouseEvent
from Window.EditHostNetargsWindow import *
from Window.EditLinkArgsWindow import EditLinkArgsWindow
from Window.EditSwitchNetargsWindow import *
import globaldata
from qdarktheme.qtpy.QtWidgets import (
    QGraphicsView,
    QMenu,
    QGraphicsPathItem,
    QGraphicsItemGroup,
    QGraphicsSceneMouseEvent,
)
from qdarktheme.qtpy.QtCore import Qt, QRect
from qdarktheme.qtpy.QtGui import QPainter, QAction, QCursor

from item import GraphicItem, HostGraphicItem, SwitchGraphicItem
from edge import Edge, GraphicEdge
from HostInfoForm import HostInfoForm
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
        self.drag_start_item = None
        # item menu
        self.item_clicked = None
        self.menu = QMenu(self)
        self.deleteAction = QAction(text="删除")
        self.deleteAction.triggered.connect(self.deleteItem)
        self.menu.addAction(self.deleteAction)

        self.hostInform = HostInfoForm(self.jobSim)
        self.init_ui()

        self.lineToolEnabled = False
        self.hostAdding = False
        self.switchAdding = False

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

    def setHostToAdd(
        self, host_name, host_type, img, width, height, onlyCpu, Host_class
    ):
        self.lineToolDisable()
        self.hostAdding = True
        self.hostToAdd_name = host_name
        self.hostToAdd_type = host_type
        self.hostToAdd_img = img
        self.hostToAdd_width = width
        self.hostToAdd_height = height
        self.hostToAdd_onlyCpu = onlyCpu
        self.hostToAdd_class = Host_class

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
        pos_x=0,
        pos_y=0,
    ):
        item = HostGraphicItem(
            host_name, host_type, img, width, height, parent=self, Host_class=Host_class
        )
        # 将onlyCpu记录到属性中
        item.hostAttr.only_cpu = onlyCpu
        item.setPos(pos_x, pos_y)
        self.jobSim.addHostItem(item, onlyCPU=onlyCpu)
        self.gr_scene.add_node(item)
        return item

    def setSwitchToAdd(
        self, switch_name, switch_type, img, width, height, Switch_class
    ):
        self.lineToolDisable()
        self.switchAdding = True
        self.switchToAdd_name = switch_name
        self.switchToAdd_type = switch_type
        self.switchToAdd_img = img
        self.switchToAdd_width = width
        self.switchToAdd_height = height
        self.switchToAdd_class = Switch_class

    def stopAdding(self):
        self.hostAdding = False
        self.switchAdding = False

    # 在画布上添加交换机
    def createGraphicSwitchItem(
        self,
        switch_name,
        switch_type,
        img,
        width,
        height,
        Switch_class=Switch,
        pos_x=0,
        pos_y=0,
    ):
        item = SwitchGraphicItem(
            switch_name,
            switch_type,
            img,
            width,
            height,
            parent=self,
            Switch_class=Switch_class,
        )
        item.setPos(pos_x, pos_y)
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

    def openHostEditor(self, item):
        if isinstance(item.hostAttr, NormalHost):
            self.editHostNetargsWindowNormal.setHostGraphicItem(item)
            self.editHostNetargsWindowNormal.show()
        if isinstance(item.hostAttr, UdpHost):
            self.editHostNetargsWindowUdp.setHostGraphicItem(item)
            self.editHostNetargsWindowUdp.show()
        if isinstance(item.hostAttr, TsnHost):
            self.editHostNetargsWindowTsn.setHostGraphicItem(item)
            self.editHostNetargsWindowTsn.show()
        if isinstance(item.hostAttr, TcpHost):
            self.editHostNetargsWindowTcp.setHostGraphicItem(item)
            self.editHostNetargsWindowTcp.show()
        if isinstance(item.hostAttr, DdsHost):
            self.editHostNetargsWindowDds.setHostGraphicItem(item)
            self.editHostNetargsWindowDds.show()
        if isinstance(item.hostAttr, RdmaHost):
            self.editHostNetargsWindowRdma.setHostGraphicItem(item)
            self.editHostNetargsWindowRdma.show()

    def graphicItemClicked(self, item, event: QGraphicsSceneMouseEvent):
        self.item_clicked = item
        if isinstance(self.item_clicked, HostGraphicItem):
            self.parent.selectHost(item)
        if isinstance(self.item_clicked, SwitchGraphicItem):
            self.parent.selectSwitch(item)
        if event.button() == Qt.MouseButton.RightButton:
            self.menu.popup(QCursor.pos())
        elif self.lineToolEnabled:
            self.lineClick()

    def linkClicked(self, link, event: QGraphicsSceneMouseEvent):
        self.item_clicked = link
        self.parent.selectLink(link)
        if event.button() == Qt.MouseButton.RightButton:
            self.menu.popup(QCursor.pos())
        return

    # 获取点击的link
    def get_link_at_pos(self, event):
        pos = event.pos()
        # item = self.itemAt(pos)
        """ 鼠标所在的10*10内都是选中范围 """
        area = QRect(pos.x() - 5, pos.y() - 5, 10, 10)
        if len(self.items(area)) == 0:
            return None
        result = self.items(area)[0]
        # if result.type() == GraphicItem.type or result.type() == QGraphicsPathItem
        if isinstance(result, QGraphicsPathItem):
            return result
        else:
            return None

    def get_items_at_rubber(self):
        """Get group select items."""
        area = self.rubberBandRect()
        return self.items(area)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            targetPos = self.mapToScene(event.pos())
            if self.hostAdding:
                self.createGraphicHostItem(
                    self.hostToAdd_name,
                    self.hostToAdd_type,
                    self.hostToAdd_img,
                    self.hostToAdd_width,
                    self.hostToAdd_height,
                    self.hostToAdd_onlyCpu,
                    self.hostToAdd_class,
                    targetPos.x(),
                    targetPos.y(),
                )
            elif self.switchAdding:
                self.createGraphicSwitchItem(
                    self.switchToAdd_name,
                    self.switchToAdd_type,
                    self.switchToAdd_img,
                    self.switchToAdd_width,
                    self.switchToAdd_height,
                    self.switchToAdd_class,
                    targetPos.x(),
                    targetPos.y(),
                )
        link = self.get_link_at_pos(event)
        if link != None:
            self.linkClicked(link, event)
        self.parent.update_tree_view()

    def lineToolStateChange(self):
        if not self.lineToolEnabled:
            self.lineToolEnable()
        else:
            self.lineToolDisable()

    def lineToolEnable(self):
        self.lineToolEnabled = True
        self.parent.ui.add_line.setText("停止连线")
        self.hostAdding = False
        self.switchAdding = False

    def lineToolDisable(self):
        self.lineToolEnabled = False
        self.parent.ui.add_line.setText("连线")

    def lineClick(self):
        item = self.item_clicked
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

    def deleteItem(self):
        # 删除键
        item = self.item_clicked
        if isinstance(item, QGraphicsItemGroup):
            self.gr_scene.remove_node(item)
        if isinstance(item, QGraphicsPathItem):
            self.gr_scene.remove_edge(item)
        self.parent.cancelSelect()
        self.parent.update_tree_view()

    # def mouseReleaseEvent(self, event):
    #         super().mouseReleaseEvent(event)
