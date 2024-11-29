import math

# from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem
# from PyQt5.QtGui import QColor, QPen, QBrush, QPainterPath
# from PyQt5.QtCore import Qt, QPointF
from qdarktheme.qtpy.QtWidgets import QGraphicsPathItem, QGraphicsItem
from qdarktheme.qtpy.QtGui import QColor, QPen, QPainterPath
from qdarktheme.qtpy.QtCore import Qt, QPointF
from entity.link import Link
import globaldata

# 线条的包装类
class Edge:

    def __init__(self, scene, start_item, end_item): # 场景、开始图元、结束图元
        super().__init__()
        self.scene = scene
        self.start_item = start_item
        self.end_item = end_item

        self.gr_edge = GraphicEdge(self)
        # # 添加进scene
        # self.scene.add_edge(self.gr_edge)

        # 连接属性
        self.linkAttr = Link(start_item, end_item, "Eth100M")
        # 添加到全局变量中
        globaldata.linkList.append(self)

        # 移到图片正中间
        if self.start_item is not None:
            self.update_positions()

    # 最终保存进scene
    def store(self):
        self.scene.add_edge(self.gr_edge)

    # 更新位置，线的端点在图片正中间
    def update_positions(self):
        # 想让线条从图元的中心位置开始，让他们都加上偏移
        patch = self.start_item.width / 2
        # src_pos 记录的是开始图元的位置，此位置为图元的左上角
        src_pos = self.start_item.pos()
        self.gr_edge.set_src(src_pos.x()+patch, src_pos.y()+patch)
        # 如果结束位置图元也存在，则做同样操作
        if self.end_item is not None:
            end_pos = self.end_item.pos()
            self.gr_edge.set_dst(end_pos.x()+patch, end_pos.y()+patch)
        else:
            self.gr_edge.set_dst(src_pos.x()+patch, src_pos.y()+patch)
        self.gr_edge.update()

    def remove_from_current_items(self):
        self.end_item = None
        self.start_item = None

    def remove_from_globaldata(self):
        i = 0
        while i < len(globaldata.linkList):
            if globaldata.linkList[i] == self:
                globaldata.linkList.pop(i)
            else:
                i += 1

    def remove(self):
        self.remove_from_current_items()
        self.scene.remove_edge(self.gr_edge)
        self.gr_edge = None


class GraphicEdge(QGraphicsPathItem):
    def __init__(self, edge_wrap: Edge, parent=None):
        super().__init__(parent)
        self.edge_wrap = edge_wrap
        self.width = 5.0
        self.pos_src = [0, 0]
        self.pos_dst = [0, 0]

        self._pen = QPen(QColor("#000"))
        self._pen.setWidthF(self.width)

        self._pen_dragging = QPen(QColor("#000"))
        self._pen_dragging.setStyle(Qt.PenStyle.DashDotLine)
        self._pen_dragging.setWidthF(self.width)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable) # 线条可选
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setZValue(-1) # 让线条出现在所有图元的最下层

    def getLinkAttr(self):
        result = {
            "link_bandwidth": self.edge_wrap.linkAttr.link_bandwidth,
        }

        return result

    def remove_from_globaldata(self):
        self.edge_wrap.remove_from_globaldata()

    def set_src(self, x, y):
        self.pos_src = [x, y]

    def set_dst(self, x, y):
        self.pos_dst = [x, y]

    def calc_path(self):
        path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))
        path.lineTo(self.pos_dst[0], self.pos_dst[1])
        return path

    def boundingRect(self):
        return self.shape().boundingRect()

    def shape(self):
        return self.calc_path()

    def paint(self, painter, graphics_item, widget=None):
        self.setPath(self.calc_path())
        path = self.path()
        if self.edge_wrap.end_item is None:
            # 包装类中存储了线条开始和结束位置的图元
        	# 刚开始拖拽线条时，并没有结束位置的图元，所以是None
        	# 这个线条画的是拖拽路径，点线
            painter.setPen(self._pen_dragging)
            painter.drawPath(path)
        else:
            # 这画的才是连接后的线
            painter.setPen(self._pen)
            painter.drawPath(path)
