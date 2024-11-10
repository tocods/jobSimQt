from realtime_draw.GUI_ui import Ui_MainWindow
from qdarktheme.qtpy.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class CustomToolbar(NavigationToolbar):
    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)

        self.keep_buttons(["Home", "Pan", "Zoom", "Save"])

    def keep_buttons(self, button_names):
        for action in self.actions():
            if action.text() not in button_names:
                self.removeAction(action)


class ResultPlot(QMainWindow):
    def __init__(self, parent=None):
        super(ResultPlot, self).__init__(parent)
        self.parent = parent
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ui.appLayout.addWidget(self.canvas)

        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        self.toolbar = CustomToolbar(self.canvas, self)
        self.ui.appLayout.addWidget(self.toolbar)

        self.ui.displayButton.clicked.connect(self.display)
        self.ui.loadButton.clicked.connect(self.loadData)

    def loadData(self):
        return

    def display(self):
        plotSelectedList = []
        for i in range(self.ui.listWidgetCheck.count()):
            item = self.ui.listWidgetCheck.item(i)
            checkbox = self.ui.listWidgetCheck.itemWidget(item)
            plotName = checkbox.text()
            if checkbox.isChecked():
                plotSelectedList.append(plotName)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_xlabel("时间(ms)")
        ax.set_ylabel("时延(ms)")
        ax.grid(True)

        maxX = 0.0
        maxY = 0.0
        for plotName in plotSelectedList:
            id = self.parent.parser.flowNameVector[plotName]
            x = self.parent.parser.latencyResultX[id]
            y = self.parent.parser.latencyResultY[id]
            ax.plot(x, y, label=plotName)
            maxX = max(maxX, self.parent.parser.latencyResultMaxX[id])
            maxY = max(maxY, self.parent.parser.latencyResultMaxY[id])
        ax.set_xlim(0, maxX)
        ax.set_ylim(0, maxY)

        ax.legend()
        self.canvas.draw()


class LatencyResultPlot(ResultPlot):
    def loadData(self):
        self.parent.parser.loadData()
        self.ui.listWidgetCheck.clear()
        for flowName in self.parent.parser.flowNameList:
            item = QListWidgetItem(self.ui.listWidgetCheck)
            checkbox = QCheckBox(flowName)
            item.setSizeHint(checkbox.sizeHint())
            self.ui.listWidgetCheck.addItem(item)
            self.ui.listWidgetCheck.setItemWidget(item, checkbox)

    def display(self):
        plotSelectedList = []
        for i in range(self.ui.listWidgetCheck.count()):
            item = self.ui.listWidgetCheck.item(i)
            checkbox = self.ui.listWidgetCheck.itemWidget(item)
            plotName = checkbox.text()
            if checkbox.isChecked():
                plotSelectedList.append(plotName)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_xlabel("时间(ms)")
        ax.set_ylabel("时延(ms)")
        ax.grid(True)

        maxX = 0.0
        maxY = 0.0
        for plotName in plotSelectedList:
            id = self.parent.parser.flowNameVector[plotName]
            x = self.parent.parser.latencyResultX[id]
            y = self.parent.parser.latencyResultY[id]
            ax.plot(x, y, label=plotName)
            maxX = max(maxX, self.parent.parser.latencyResultMaxX[id])
            maxY = max(maxY, self.parent.parser.latencyResultMaxY[id])
        ax.set_xlim(0, maxX)
        ax.set_ylim(0, maxY)

        ax.legend()
        self.canvas.draw()


class BufferResultPlot(ResultPlot):
    def loadData(self):
        self.parent.parser.loadData()
        self.ui.listWidgetCheck.clear()
        for hostName, _ in self.parent.parser.hostNameVector.items():
            item = QListWidgetItem(self.ui.listWidgetCheck)
            checkbox = QCheckBox(hostName)
            item.setSizeHint(checkbox.sizeHint())
            self.ui.listWidgetCheck.addItem(item)
            self.ui.listWidgetCheck.setItemWidget(item, checkbox)

    def display(self):
        plotSelectedList = []
        for i in range(self.ui.listWidgetCheck.count()):
            item = self.ui.listWidgetCheck.item(i)
            checkbox = self.ui.listWidgetCheck.itemWidget(item)
            plotName = checkbox.text()
            if checkbox.isChecked():
                plotSelectedList.append(plotName)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_xlabel("时间(ms)")
        ax.set_ylabel("缓冲区")
        ax.grid(True)

        maxX = 0.0
        maxY = 0.0
        for plotName in plotSelectedList:
            id = self.parent.parser.hostNameVector[plotName]
            x = self.parent.parser.bufferResultX[id]
            y = self.parent.parser.bufferResultY[id]
            ax.scatter(x, y, label=plotName)
            maxX = max(maxX, self.parent.parser.bufferResultMaxX[id])
            maxY = max(maxY, self.parent.parser.bufferResultMaxY[id])
        ax.set_xlim(0, maxX)
        ax.set_ylim(0, maxY)

        ax.legend()
        self.canvas.draw()
