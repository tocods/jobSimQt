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
        # 读取文件 
        # id_type_dict: vector_id(比如87) => vector_type(标签，比如“数据包时延”) 的映射
        # id_points: vector_id(比如87) => points(数据点集，比如[[0,1],[2,5]]) 的映射
        self.id_type_dict, self.id_points = read_file() 
        # 在GUI界面上插入绘图选项，即vector_type标签
        self.showList() 

        # 创建figure
        self.pic = App() 
        # 创建画布,内容为figure
        self.canvas = FigureCanvasQTAgg(self.pic.fig)
        # self.mpl_ntb = NavigationToolbar(self.canvas, self)  # 添加完整的 toolbar,增加图片放大、移动的按钮
        # 四个tool图标：“复原 移动 放大 截图”
        self.mpl_ntb = self.pic.toolbar 

        # 将画布和tool栏放置到GUI界面
        self.appLayout.addWidget(self.canvas)
        self.appLayout.addWidget(self.mpl_ntb)

        # 功能按钮
        self.displayButton.clicked.connect(self.display)
        self.pauseButton.clicked.connect(self.run_pause)
        self.stopButton.clicked.connect(self.stop)
        # self.resetButton.clicked.connect(self.reset)

    def display(self):
        self.reset()
        # choose_id_lr_dict = self.getChoose() #左坐标轴/右坐标轴，比如“{'0x328009e': 'R', '0x32b00b5': 'L'}
        choose_id_list = self.id_type_dict.keys() #choose_id_lr_dict.keys()
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
            '''
            # 根据用户选择的'L'或'R'来分别加入到不同的list
            if choose_id_lr_dict[id] == 'L':
                data_list_l.append(self.id_points[int(id, 10)])
                name_list_l.append(id)
            else:
                data_list_r.append(self.id_points[int(id, 10)])
                name_list_r.append(id)
            '''
        # 传入数据执行
        self.pic.run(data_list_l, data_list_r, name_list_l, name_list_r)
        self.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        # self.canvas.flush_events()  # 画布刷新self.figs.canvas

    def reset(self):
        self.pic.reset()

    def run_pause(self):
        self.pic.run_pause()

    def stop(self):
        self.pic.stop()

    # 用于展示左侧选择列表
    def showList(self):
        self.insert(sorted(self.id_points.keys()))

    # 用于插入列表项
    def insert(self, data_list):
        """
             :param list: 要插入的选项文字数据列表 list[str] eg：['城市'，'小区','小区ID']
             """
        for i in data_list:
            if len(self.id_points[i]) < 100:
                continue
            check_box = QCheckBox(self.id_type_dict[i]) # QCheckBox(str(i) + ',' + self.id_type_dict[i])  # 实例化一个QCheckBox，把文字传进去

            # combo_box = QComboBox(self)
            # # 用于指示线条指示的坐标轴左右
            # items = ['L', 'R']
            # combo_box.addItems(items)

            item1 = QListWidgetItem()  # 实例化一个Item，QListWidget，不能直接加入QCheckBox
            self.listWidgetCheck.addItem(item1)  # 把QListWidgetItem加入QListWidget
            self.listWidgetCheck.setItemWidget(item1, check_box)  # 再把QCheckBox加入QListWidgetItem

            # item2 = QListWidgetItem()  # 实例化一个Item，QListWidget，不能直接加入QComboBox
            # self.listWidgetCombo.addItem(item2)  # 把QListWidgetItem加入QListWidget
            # self.listWidgetCombo.setItemWidget(item2, combo_box)  # 再把QComboBox加入QListWidgetItem

    # 用于测试列表选择框
    # def getChoose(self) -> [str]:
    #     """
    #     得到备选统计项的字段
    #     :return: list[str]
    #     """
    #     count = self.listWidgetCheck.count()  # 得到QListWidget的总个数
    #     cb_list = [self.listWidgetCheck.itemWidget(self.listWidgetCheck.item(i))
    #                for i in range(count)]  # 得到QListWidget里面所有QListWidgetItem中的QCheckBox
    #     # comb_list = [self.listWidgetCombo.itemWidget(self.listWidgetCombo.item(i))
    #     #            for i in range(count)]  # 得到QListWidget里面所有QListWidgetItem中的QComboBox

    #     # print(cb_list)
    #     chooses = {}  # 存放被选择的数据及类型
    #     for i in range(count):
    #         if cb_list[i].isChecked():
    #             # TT类型消息显示右边坐标轴'R'
    #             id = cb_list[i].text().split(',')[0]    # 获取十六进制的id
    #             if self.id_type_dict[int(id, 10)] == 'TT':
    #                 chooses[id] = 'R'
    #             else:
    #                 chooses[id] = 'L'

    #             # chooses[cb_list[i].text()] = comb_list[i].currentText()
    #     # print(chooses)
    #     return chooses


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ui = CamShow()
#     ui.show()
#     sys.exit(app.exec())
