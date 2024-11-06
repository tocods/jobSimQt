from realtime_draw.GUI_ui import Ui_MainWindow
import sys
from qdarktheme.qtpy.QtWidgets import *
from realtime_draw.parserModule import read_file
from realtime_draw.app import App
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg                            # pyqt5的画布
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class CamShow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(CamShow, self).__init__(parent)
        self.setupUi(self)
        self.id_type_dict, self.id_points = read_file() 
        self.showList() 

        self.pic = App() 
        self.canvas = FigureCanvasQTAgg(self.pic.fig)
        self.mpl_ntb = self.pic.toolbar 

        self.appLayout.addWidget(self.canvas)
        self.appLayout.addWidget(self.mpl_ntb)

        self.displayButton.clicked.connect(self.display)
        self.pauseButton.clicked.connect(self.run_pause)
        self.stopButton.clicked.connect(self.stop)

    def display(self):
        self.reset()
        choose_id_list = self.id_type_dict.keys()
        if len(choose_id_list) == 0:
            QMessageBox.information(self, "警告", "请选择至少一个数据！")
            return
        data_list_l = []
        data_list_r = []
        name_list_l = []
        name_list_r = []
        for id in choose_id_list:
            # print(self.id_points[int(id, 10)])
            # =================================
            # 对过少的数据不进行仿真,查id时注意oct和hex的转换
            if len(self.id_points[id]) < 100:
                QMessageBox.information(self, "警告", id + "类消息数据过少，只有" + str(len(self.id_points[id])) + '条！')
                continue
            name_list_l.append(id)
            data_list_l.append(self.id_points[id])

        self.pic.run(data_list_l, data_list_r, name_list_l, name_list_r)
        self.canvas.draw()

    def reset(self):
        self.pic.reset()

    def run_pause(self):
        self.pic.run_pause()

    def stop(self):
        self.pic.stop()

    def showList(self):
        self.insert(sorted(self.id_points.keys()))

    def insert(self, data_list):
        for i in data_list:
            if len(self.id_points[i]) < 100:
                continue
            check_box = QCheckBox(self.id_type_dict[i]) # QCheckBox(str(i) + ',' + self.id_type_dict[i])  # 实例化一个QCheckBox，把文字传进去

            item1 = QListWidgetItem()
            self.listWidgetCheck.addItem(item1)
            self.listWidgetCheck.setItemWidget(item1, check_box)
