from qdarktheme.qtpy.QtWidgets import QWidget
from show_net_results_ui import Ui_Dialog
from realtime_draw.parserModule import ParserModule
import globaldata
import os
import re
from net import Ui_Net
from realtime_draw.ResultPlot import LatencyResultPlot, BufferResultPlot, LossResultPlot
from component.netanalysis import Ui_NetAnalysis

class ShowNetResultsWindow(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.parent = parent
        self.ui = Ui_Net()
        self.ui.setupUi(self)
        self.latency = LatencyResultPlot(self)
        self.latency.setObjectName("latency")
        self.ui.tabWidget.addTab(self.latency, "时延")
        self.buffer = BufferResultPlot(self)
        self.buffer.setObjectName("buffer")
        self.ui.tabWidget.addTab(self.buffer, "缓冲区")
        self.loss = LossResultPlot(self)
        self.buffer.setObjectName("loss")
        self.ui.tabWidget.addTab(self.loss, "丢包率")


        self.netCal = QWidget()
        self.netCalUi = Ui_NetAnalysis()
        self.netCalUi.setupUi(self.netCal)
        self.ui.tabWidget.addTab(self.netCal, "网络演算")
        self.setWindowTitle("仿真结果曲线")
        path = globaldata.currentProjectInfo.path
        self.parser = ParserModule(path)
        
    def reload(self):
        path = globaldata.currentProjectInfo.path

        self.parser = ParserModule(path)
