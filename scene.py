import math

# from PyQt5.QtWidgets import QGraphicsScene
# from PyQt5.QtGui import QColor, QPen
# from PyQt5.QtCore import QLine, Qt
from qdarktheme.qtpy.QtWidgets import QGraphicsScene
from qdarktheme.qtpy.QtGui import QColor, QPen


class GraphicScene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)
        # settings
        self.grid_size = 20
        self.grid_squares = 5

        # self._color_background = QColor('#D3D3D3') #颜色表格 https://blog.csdn.net/yc__coder/article/details/107371082
        self._color_light = QColor('#2f2f2f')
        self._color_dark = QColor('#292929')

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        # self.setBackgroundBrush(self._color_background)
        self.setSceneRect(0, 0, 500, 500)

        self.nodes = []
        self.edges = []

    # 在画布上添加图像图元
    def add_node(self, node):
        self.nodes.append(node)
        self.addItem(node)
    # 删除画布上的某图像图元
    def remove_node(self, node):
        try:
            node.remove_from_globaldata()
            self.nodes.remove(node)
            # 删除图元时，遍历与其连接的线，并移除
            for edge in self.edges:
                if edge.edge_wrap.start_item is node or edge.edge_wrap.end_item is node:
                    self.remove_edge(edge)
            self.removeItem(node)
        except Exception as reason:
            reason #请勿连续按下删除键
    # 在画布上添加连线图元
    def add_edge(self, edge):
        self.edges.append(edge)
        self.addItem(edge)
    # 删除画布上的某连线图元
    def remove_edge(self, edge):
        try:
            self.edges.remove(edge)
            self.removeItem(edge)
        except Exception as reason:
            reason #请勿连续按下删除键

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
