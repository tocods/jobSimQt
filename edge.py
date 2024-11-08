import math

# from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem
# from PyQt5.QtGui import QColor, QPen, QBrush, QPainterPath
# from PyQt5.QtCore import Qt, QPointF
from qdarktheme.qtpy.QtWidgets import QGraphicsPathItem, QGraphicsItem
from qdarktheme.qtpy.QtGui import QColor, QPen, QPainterPath
from qdarktheme.qtpy.QtCore import Qt, QPointF

class Link:
    name_registry = {}
    def __init__(self, endpoint1, endpoint2, type):
        self.set_name('Link')

        # 连接属性，初始化为默认值
        self.link_bandwidth = 100

        self.endpoint1 = endpoint1  # 连接一端
        self.endpoint2 = endpoint2  # 连接另一端
        self.type = type

    def set_name(self, name):
        # TODO: 检查名字是否符合omnet规范
        # 检查是否重名
        if name in Link.name_registry:         
            Link.name_registry[name] += 1
            # 当重名时，自动加上编号

            # 如果加编号后不重名了
            if not name + str(Link.name_registry[name]) in Link.name_registry:
                self.name = name + str(Link.name_registry[name])
                Link.name_registry.update({name + str(Link.name_registry[name]): 1})
            # 如果加编号后还是重名，继续加编号，递归调用
            else:
                self.set_name(name)

        else:
            self.name = name
            Link.name_registry.update({name: 1})


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
        #globaldata.linkList.append(self)

        # 移到图片正中间
        if self.start_item is not None:
            self.update_positions()

    # 最终保存进scene
    def store(self):
        self.scene.addItem(self.gr_edge)

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

    def remove(self):
        self.remove_from_current_items()
        self.scene.remove_edge(self.gr_edge)
        self.gr_edge = None


class GraphicEdge(QGraphicsPathItem):

    def __init__(self, edge_wrap, parent=None):
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
