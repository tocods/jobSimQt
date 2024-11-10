from qdarktheme.qtpy.QtWidgets import QWidget
from show_net_results_ui import Ui_Dialog
from realtime_draw.parserModule import ParserModule
import globaldata
import os
import re
from net import Ui_Net
from realtime_draw.ResultPlot import LatencyResultPlot
from realtime_draw.ResultPlot import BufferResultPlot
from component.netanalysis import Ui_NetAnalysis

class ShowNetResultsWindow(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.parent = parent
        self.ui = Ui_Net()
        self.ui.setupUi(self)
        self.latency = LatencyResultPlot(self)
        self.latency.setObjectName("model")
        self.ui.tabWidget.addTab(self.latency, "时延曲线")
        self.buffer = BufferResultPlot(self)
        self.buffer.setObjectName("develop")
        self.ui.tabWidget.addTab(self.buffer, "缓冲区曲线")

        self.netCal = QWidget()
        self.netCalUi = Ui_NetAnalysis()
        self.netCalUi.setupUi(self.netCal)
        self.ui.tabWidget.addTab(self.netCal, "网络演算")
        self.setWindowTitle("仿真结果曲线")
        path = globaldata.currentProjectInfo.path
        with open(os.path.join(path, "Parameters.ini"), "r", encoding="utf-8") as file:
            configText = file.read()
            flowNameList = re.findall(r'\bflowName\s*=\s*"([^"]+)"', configText)
        self.parser = ParserModule(
            os.path.join(path, "results", "General-#0.vec"), flowNameList
        )
    def reload(self):
        path = globaldata.currentProjectInfo.path
        with open(os.path.join(path, "Parameters.ini"), "r", encoding="utf-8") as file:
            configText = file.read()
            flowNameList = re.findall(r'\bflowName\s*=\s*"([^"]+)"', configText)
        self.parser = ParserModule(
            os.path.join(path, "results", "General-#0.vec"), flowNameList
        )
