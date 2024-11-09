from qdarktheme.qtpy.QtWidgets import QWidget
from show_net_results_ui import Ui_Dialog
from realtime_draw.parserModule import ParserModule
import globaldata
import os
import re


class ShowNetResultsWindow(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("仿真结果曲线")
        path = globaldata.currentProjectInfo.path
        with open(os.path.join(path, "Parameters.ini"), "r", encoding="utf-8") as file:
            configText = file.read()
            flowNameList = re.findall(r'\bflowName\s*=\s*"([^"]+)"', configText)
        self.parser = ParserModule(
            os.path.join(path, "results", "General-#0.vec"), flowNameList
        )
