from qdarktheme.qtpy.QtWidgets import QWidget
from show_net_results_ui import Ui_Dialog
from realtime_draw.QtUI import CamShow


class ShowNetResultsWindow(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("仿真结果曲线")
        self.hide()
