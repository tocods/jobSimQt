from realtime_draw.GUI_ui import Ui_MainWindow
from qdarktheme.qtpy.QtWidgets import *
from realtime_draw.parserModule import read_file
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import globaldata
import os


class LatencyResult(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(LatencyResult, self).__init__(parent)
        self.setupUi(self)
        self.id_type_dict, self.id_points = read_file()
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.appLayout.addWidget(self.canvas)

        plt.rcParams['toolbar'] = 'toolmanager'

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        tmp = plt.gcf().canvas.manager.toolbar
        tmp.remove_toolitem('forward')
        tmp.remove_toolitem('back')
        tmp.remove_toolitem('subplots')
        tmp.remove_toolitem('help')
        tmp.remove_toolitem('home')
        tmp.remove_toolitem('pan')
        tmp.remove_toolitem('zoom')
        self.toolbar = tmp
        self.appLayout.addWidget(self.toolbar)

        self.displayButton.clicked.connect(self.display)
        self.pauseButton.clicked.connect(self.toggle_pause)
        self.stopButton.clicked.connect(self.stop_animation)
        self.anim = None
        self.paused = False
        self.x = []
        self.y = []
        self.max_x = 0.0
        self.max_y = 0.0

        self.time = 500

    def readData(self):
        self.x = []
        self.y = []
        self.max_x = 0.0
        self.max_y = 0.0
        project = globaldata.currentProjectInfo.path
        data_path = os.path.join(project, "results", "General-#0.vec")
        vector_id = -1
        with open(data_path, "r", encoding="utf-8") as fp:
            while True:
                try:
                    line = fp.readline()
                    if line == "":
                        return
                    if line.find("meanBitLifeTimePerPacket") > 0:  # vector 87 ......
                        strlist = line.split(" ")
                        vector_id = int(strlist[1])
                        break
                    continue
                except:
                    continue
        x = []
        y = []
        with open(data_path, "r", encoding="utf-8") as fp:
            while True:
                try:
                    line = fp.readline()
                    if line == "":
                        break
                    # 忽略无效行
                    if line.find(f"{vector_id}\t") != 0:
                        continue
                    line_list = line.strip("\n").split("\t")
                    if len(line_list) != 4:
                        continue
                    id = int(line_list[0])  # id
                    print(f"id:{id}, line_list:{line_list}")
                    self.x.append(float(line_list[2]) * 1000)
                    self.y.append(float(line_list[3]) * 1000)
                    self.max_x = max(self.max_x, float(line_list[2]) * 1000)
                    self.max_y = max(self.max_y, float(line_list[3]) * 1000)
                except:
                    continue

    def animate_plot(self):
        self.readData()
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        print(self.max_x)
        ax.set_xlim(0, self.max_x)
        ax.set_ylim(0, self.max_y)
        ax.legend()
        ax.grid()
        (line,) = ax.plot([], [], "r-", animated=True)

        pointPerFrame = max(1, int(len(self.x) / self.time))
        print(pointPerFrame)
        def update(frame):
            right = min(len(self.x), frame * pointPerFrame)
            line.set_data(self.x[:right], self.y[:right])
            return (line,)

        self.anim = FuncAnimation(
            self.figure,
            update,
            frames=int(len(self.x) / pointPerFrame) + 1,
            interval=1,
            blit=True,
            repeat=False,
        )
        self.canvas.draw()

    def toggle_pause(self):
        if self.anim:
            if self.paused:
                self.anim.event_source.start()
            else:
                self.anim.event_source.stop()
            self.paused = not self.paused

    def stop_animation(self):
        if self.anim:
            self.anim.event_source.stop()
            self.anim.event_source.start()
            self.figure.clear()
            self.canvas.draw()

    def display(self):
        self.animate_plot()
        self.canvas.draw()
