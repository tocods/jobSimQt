# ---------------------------------------------------------------------------------------------
#  Copyright (c) Yunosuke Ohsugi. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------*/

import sys
import json
import subprocess
import os
import numpy as np
from scipy import stats
import random
from functools import partial
import project
import qdarktheme
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot, QRegularExpression
from qdarktheme.qtpy.QtGui import *
from qdarktheme.qtpy.QtWidgets import *
from main_ui import UI
from component.start import Ui_start
from util.jobSim import sysSim, ParseUtil, HostInfo, CPUInfo, GPUInfo, VideoCardInfo, JobInfo, CPUTaskInfo, GPUTaskInfo, FaultGenerator, tranFromC2E, tranFromE2C
from jobSimPage import JobSimPage
from component.hostinfo import Ui_HostInfo
from component.jobinfo import Ui_JobInfo
from component.faultinfo import Ui_FaultInfo
from PySide6.QtCharts import QChart,QChartView,QLineSeries,QDateTimeAxis,QValueAxis, QPieSeries
from jobSimPainter import Painter, XmlParser
from util.table import NumericDelegate
import globaldata

class JobSimQt(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.start = Ui_start()
        self.start.setupUi(self)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("系统管理仿真与建模平台")
        self.setWindowIcon(QIcon("img/仿真.png"))
        self.center()
        self.history = []
        globaldata.readPath()
        i = 0
        f = QFont()
        f.setPointSize(13)
        self.start.projects.setFont(f)
        self.start.projects.setHeaderHidden(True)
        self.start.projects.clicked.connect(self.choseP)
        with open("history.txt", "r") as f:
            for line in f.readlines():
                if i > 10:
                    break
                self.history.append(line)
                i = i + 1
                item = QTreeWidgetItem([line.strip('\n')])
                self.start.projects.addTopLevelItem(item)
        self.start.newP.clicked.connect(self.newP)
        self.start.openP.clicked.connect(self.openP)
        self.start.shutdown.clicked.connect(sys.exit)


    """
    创建一个新的项目目录并使用默认的 JSON 文件进行初始化。

    该方法打开一个目录选择对话框供用户选择目录。
    然后在所选目录中创建三个 JSON 文件（'hosts.json'、'jobs.json' 和 'faults.json'），
    每个文件都初始化为空列表。所选目录路径将添加到历史记录中，并将历史记录保存到 'history.txt'。
    最后，它调用 startUp 方法并传入所选目录路径。

    异常:
        IOError: 如果写入 JSON 文件或历史记录文件时发生错误。
    """
    def newP(self):
        file_name = QFileDialog.getExistingDirectory(None, "Open File", "")
        print(file_name)
        with open(file_name + "/hosts.json", "w") as f:
            f.write("[]")
        with open(file_name + "/jobs.json", "w") as f:
            f.write("[]")
        with open(file_name + "/faults.json", "w") as f:
            f.write("[]")
        l = file_name + '\n'
        if l in self.history:
            self.history.remove(file_name + '\n')
        self.history.insert(0, file_name + '\n')
        with open("history.txt", "w") as f:
            f.writelines(self.history)
        self.startUp(file_name)
    

    """
    打开一个项目目录并使用 JSON 文件进行初始化。

    该方法接受一个项目目录路径作为参数。
    如果项目目录不存在，则显示一个消息框并返回。
    如果项目目录中的任何 JSON 文件不存在，则显示一个消息框并返回。
    否则，将项目目录路径添加到历史记录中，并将历史记录保存到 'history.txt'。
    最后，它调用 startUp 方法并传入项目目录路径。
    """
    def openP(self):
        file_name = QFileDialog.getExistingDirectory(None, "Open File", "")
        print(file_name)
        self.openProject(file_name)

    """
    打开一个项目目录并使用 JSON 文件进行初始化。

    该方法接受一个项目目录路径作为参数。
    如果项目目录不存在，则显示一个消息框并返回。
    如果项目目录中的任何 JSON 文件不存在，则显示一个消息框并返回。
    否则，将项目目录路径添加到历史记录中，并将历史记录保存到 'history.txt'。
    最后，它调用 startUp 方法并传入项目目录路径。
    """
    def openProject(self, file_name):
        if not os.path.isdir(file_name):
            QMessageBox.information(self, "", "项目不存在")
            l = file_name + '\n'
            print("is:" + l)
            if l in self.history:
                self.history.remove(l)
            with open("history.txt", "w") as f:
                f.writelines(self.history)
            print("aaab")
            self.start.projects.clear()
            for his in self.history:
                item = QTreeWidgetItem([his.strip('\n')])
                self.start.projects.addTopLevelItem(item)
                print('add' + his)
            print('nnn')
            return
        if not os.path.exists(file_name + "/hosts.json"):
            QMessageBox.information(self, "", "主机信息文件不存在")
            return
        if not os.path.exists(file_name + "/jobs.json"):
            QMessageBox.information(self, "", "任务信息文件不存在")
            return
        if not os.path.exists(file_name + "/hosts.json"):
            QMessageBox.information(self, "", "故障模型信息文件不存在")
            return
        l = file_name + '\n'
        if l in self.history:
            self.history.remove(file_name + '\n')
        self.history.insert(0, file_name + '\n')
        with open("history.txt", "w") as f:
            f.writelines(self.history)
        self.startUp(file_name)

    """
    选择项目。

    该方法获取当前项目目录树中的项目名称。
    如果项目名称是根节点，则返回。
    否则，调用 openProject 方法并传入项目名称。
    """
    def choseP(self):
        print("aaa")
        if_root = False
        #获取点击item所属根节点的名称（如无根节点则返回自身）
        nowClect = self.start.projects.currentItem().parent()
        if nowClect is None:
            if_root = True
            nowClect = self.start.projects.currentItem()
        print(nowClect.text(0))
        if not if_root:
            return
        self.openProject(nowClect.text(0))

    """
    启动应用程序并初始化所有组件和 UI 元素。

    该方法接受一个项目目录路径作为参数。
    如果项目目录路径不是绝对路径，则将其转换为绝对路径。
    然后，将项目目录路径设置为 projectPath 属性。

    该方法初始化以下组件和 UI 元素：
    - duration 属性设置为 100。
    - wfont 属性设置为 QFont 对象，字体大小设置为 30。
    - 设置字体为 wfont。
    - projectPath 属性设置为 path 的副本。
    - 调用 _initJsonFiles 方法。
    - nowClect 属性设置为 None。
    - 创建 UI 对象。
    - 调用 UI 对象的 setup_ui 方法并传入自身。
    - 为 action_change_home、action_change_dock、action_software、action_open_folder 和 action_open_color_dialog 信号连接槽。
    - 为 action_open_font_dialog 信号连接槽。
    - 为 action_out 信号连接槽。
    - 为 action_enable 和 action_disable 信号连接槽。
    - 为 actions_theme 列表中的每个动作连接槽。
    - 获取屏幕对象。
    - 获取屏幕可用区域大小。
    - 设置 homeui 和 resultui 的 infoList 表头隐藏。
    - 设置窗口大小。
    - 调用 _initAll 方法。
    - 调用 initTreeView 方法。
    - 调用 setClicked 方法。
    - 调用 center 方法。
    - 设置 currentProjectInfo 的 fullname 属性为 path。
    - 调用 network_editor 对象的 load_network_from_xml 方法。
    """
    def startUp(self, path):
        self.duration = 100
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        self.wfont = QFont()
        self.wfont.setPointSize(30)
        self.setFont(self.wfont)
        project.projectPath = path[:]
        sysSim.setPath(path)
        self._initJsonFiles()
        # 取消标题栏
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.nowClect = None
        self._ui = UI()
        self._ui.setup_ui(self)

        # Signal
        self._ui.action_change_home.triggered.connect(self._change_page)
        self._ui.action_change_dock.triggered.connect(self._change_page)
        self._ui.action_software.triggered.connect(self._change_page)
        self._ui.action_open_folder.triggered.connect(self.loadFromProject
            #lambda: QFileDialog.getOpenFileName(self, "Open File", options=QFileDialog.Option.DontUseNativeDialog)
        )
        self._ui.action_open_color_dialog.triggered.connect(
            self.saveToProject
        )
        self._ui.action_open_font_dialog.triggered.connect(
            self.setDuration
        )
        self._ui.action_out.triggered.connect(sys.exit)
        # self._ui.action_enable.triggered.connect(self._toggle_state)
        # self._ui.action_disable.triggered.connect(self._toggle_state)
        for action in self._ui.actions_theme:
            action.triggered.connect(self._change_theme)
        screen = QGuiApplication.screens()[0]
        screen_size = screen.availableGeometry()
        sysSim.setScreenSize(screen_size)
        self._ui.homeui.infoList.setHeaderHidden(True)
        self.setGeometry(0, 0, screen_size.width() * 0.9, screen_size.height() * 0.9)
        # self._ui.homeui.layoutWidget.setGeometry(0, 0, screen_size.width() * 0.8, screen_size.height() * 0.8)
        # self._ui.resultui.layoutWidget.setGeometry(0, 0, screen_size.width() * 0.8, screen_size.height() * 0.8)
        self.tsnQueueApple = QPushButton("tsn队列编辑")
        self._initAll()
        self.initTreeView()
        self.setClicked()
        self.center()

        globaldata.currentProjectInfo.setFullname(path)
        self._ui.network_editor.load_network_from_xml()

    def center(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    @Slot()
    def _change_page(self) -> None:
        action_name = self.sender().text()
        #self._ui.stack_widget.setCurrentIndex(0 if action_name == "运行仿真" else 1)
        if action_name == "系统管理评估平台":
            print(f"{globaldata.targetPath[3]} {project.projectPath} -1")
            os.popen(f"{globaldata.targetPath[3]} {project.projectPath} -1")
        if action_name == "系统管理集成开发平台":
            self._startSoftware()

    @Slot()
    def _toggle_state(self) -> None:
        state = self.sender().text()
        self._ui.central_window.centralWidget().setEnabled(state == "Enable")
        self._ui.action_enable.setEnabled(state == "Disable")
        self._ui.action_disable.setEnabled(state == "Enable")
        self.statusBar().showMessage(state)

    @Slot()
    def _change_theme(self) -> None:
        theme = self.sender().text()
        if theme == "黑色":
            theme = "dark"
        elif theme == "白色":
            theme = "light"
        QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet(theme))

    def _startSoftware(self):
        os.popen(f"{globaldata.targetPath[1]} {globaldata.targetPath[2]}")
        return

    def setClicked(self):
        # self._ui.homeui.add.clicked.connect(self._add)
        # self._ui.homeui.add.setIcon(QIcon("img/加.png"))
        # self._ui.homeui.pushButton.clicked.connect(self._delete)
        # self._ui.homeui.pushButton.setIcon(QIcon("img/减少.png"))
        # self._ui.homeui.textEdit.setReadOnly(True)
        # self._ui.homeui.run.clicked.connect(self._run)
        # self._ui.homeui.infoList.clicked.connect(self._showInfo)
        return

    def saveToProject(self):
        hosts_json = json.dumps([host.__dict__ for host in sysSim.hosts.values()], indent=4, default=lambda o: o.__dict__)
        with open(project.projectPath + "/hosts.json", 'w') as write_f:
            write_f.write(hosts_json)
        jobs_json = json.dumps([job.__dict__ for job in sysSim.jobs.values()], indent=4, default=lambda o: o.__dict__)
        with open(project.projectPath + "/jobs.json",'w') as write_f:
            write_f.write(jobs_json)
        fault_json = json.dumps([fault.__dict__ for fault in sysSim.faults.values()], indent=4, default=lambda o: o.__dict__)
        with open(project.projectPath + "/faults.json", 'w') as write_f:
            write_f.write(fault_json)
        
        globaldata.save_data()

    def setDuration(self):
        self.timewidget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("仿真时间")
        layout.addWidget(label)
        duration = QSpinBox()
        duration.setRange(0, 6000)
        duration.setSingleStep(10)
        duration.setValue(100)
        layout.addWidget(duration)
        button = QPushButton("确定")
        button.clicked.connect(partial(self._setDuration, duration))
        layout.addWidget(button)
        self.timewidget.setLayout(layout)
        self.timewidget.show()

    def _setDuration(self, duration):
        self.duration = duration.value()
        print(self.duration)

    def loadFromProject(self):
        file_name = QFileDialog.getExistingDirectory(None, "Open File", "")
        print(file_name)
        project.projectPath = file_name
        sysSim.setPath(file_name)
        globaldata.currentProjectInfo.setFullPath(file_name)
        self._ui.network_editor.load_network_from_xml()
        self._initJsonFiles()
        self._initAll()
        self.initTreeView()
        self._ui.stack_widget.setCurrentIndex(0)
        # self._ui.resultui.hostTabs.clear()
        # self._ui.resultui.jobTabs.clear()
        # self._ui.resultui.faultTabs.clear()
        # self._ui.resultui.show.setChart(QChart())
        # self._ui.resultui.showCPU.setChart(QChart())
        # self._ui.resultui.showRam.setChart(QChart())
        # self._ui.resultui.showGPU.setChart(QChart())
        # self._ui.resultui.faultResultAnalysis.setChart(QChart())
        # self._ui.resultui.jobResultAnalysis.setChart(QChart())

        #self.setClicked()
    
    
    def _initJsonFiles(self):
        if not os.path.exists(project.projectPath + "/hosts.json"):
            with open(project.projectPath + "/hosts.json", "w") as f:
                f.write("[]")
        if not os.path.exists(project.projectPath + "/jobs.json"):
            with open(project.projectPath + "/jobs.json", "w") as f:
                f.write("[]")
        if not os.path.exists(project.projectPath + "/faults.json"):
            with open(project.projectPath + "/faults.json", "w") as f:
                f.write("[]")
    
    """
    初始化应用程序的所有组件和UI元素。
    此方法执行以下任务：
    - 打印初始化消息和当前项目路径。
    - 在主页UI文本编辑小部件中设置初始文本。
    - 将当前主机、任务和故障重置为None。
    - 清空系统仿真字典中的主机、任务和故障。
    - 清空主页UI选项卡小部件。
    - 从各自的JSON文件中解析并加载主机、任务和故障。
    - 初始化并设置主机信息页面UI。
    - 在主机信息页面添加CPU、RAM和GPU利用率图表的选项卡。
    - 初始化并设置任务信息页面UI。
    - 在主页UI选项卡小部件中添加任务信息的选项卡。
    - 初始化并设置故障信息页面UI。
    - 在故障信息页面添加故障注入模型和错误报告的选项卡。
    - 隐藏主页UI选项卡小部件的选项卡栏。
    """
    def _initAll(self):
        print("init all")
        print(project.projectPath)
        self._ui.homeui.textEdit.setText("加载成功,当前项目: " + project.projectPath)
        self.nowHost = None
        self.nowJob = None
        self.nowFault = None
        sysSim.hosts = {}
        sysSim.jobs = {}
        sysSim.faults = {}
        self._ui.homeui.tabWidget.clear()
        path = project.projectPath + "/hosts.json"
        parser = ParseUtil()
        self.hosts = parser.parseHosts(path)
        for host in self.hosts:
            sysSim.hosts[host.name] = host
        path = project.projectPath + "/jobs.json"
        self.jobs = parser.parseJobs(path)
        for job in self.jobs:
            sysSim.jobs[job.name] = job
        path = project.projectPath + "/faults.json"
        self.faults = parser.parseFaults(path)
        for fault in self.faults:
            print(fault.name)
            sysSim.faults[fault.name] = fault

        w = QWidget()
        self.hostInfoPage = Ui_HostInfo()
        self.hostInfoPage.setupUi(w)
        self.hostInfoPage.pushButton.setIcon(QIcon("img/加.png"))
        self.hostInfoPage.apply.clicked.connect(self._applyHost)
        self.hostInfoPage.pushButton.clicked.connect(self._addGpu)
        self._ui.homeui.tabWidget.addTab(w, "主机")
        self.cpushow = QChartView()
        self.ramshow = QChartView()
        self.gpushow = QChartView()
        self.hostInfoPage.shows.addTab(self.cpushow, "CPU利用率")
        self.hostInfoPage.shows.addTab(self.ramshow, "内存利用率")
        self.hostInfoPage.shows.addTab(self.gpushow, "GPU利用率")
        screesize = self._ui.homeui.tabWidget.size()
        #w.setGeometry(0, 0, screesize.width(), screesize.height())

        j = QWidget()
        self.jobInfoPage = Ui_JobInfo()
        self.jobInfoPage.setupUi(j)
        self.jobInfoPage.pushButton.setIcon(QIcon("img/加.png"))
        self.jobInfoPage.apply.clicked.connect(self._applyJob)
        self.jobInfoPage.pushButton.clicked.connect(self._addKernel)
        self._ui.homeui.tabWidget.addTab(j, "任务")
        #j.setGeometry(0, 0, screesize.width(), screesize.height())

        f = QWidget()
        self.faultInfoPage = Ui_FaultInfo()
        self.faultInfoPage.setupUi(f)
        self.faultInfoPage.apply.clicked.connect(self._applyFault)
        self.showFaults = QWidget()
        self.verticalLayout = QVBoxLayout()
        self.showFaultInject = QChartView()
        self.verticalLayout.addWidget(self.showFaultInject)
        self.showFaultInject2 = QChartView()
        self.verticalLayout.addWidget(self.showFaultInject2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.showFaults.setLayout(self.verticalLayout)
        self.faultInfoPage.shows.addTab(self.showFaults, "故障注入模型")
        self.faultRecordTable = QTableWidget()
        self.faultInfoPage.shows.addTab(self.faultRecordTable, "错误上报")
        self._ui.homeui.tabWidget.addTab(f, "故障")
        #f.setGeometry(0, 0, screesize.width(), screesize.height())

        self._ui.homeui.tabWidget.tabBar().hide()
        #self._initResult()



    def initTreeView(self):
        # f = QFont()
        # f.setPointSize(10)
        # self._ui.homeui.infoList.setFont(f)
        # # 删除所有节点
        # self._ui.homeui.infoList.clear()
        # print("init tree")
        # itemhost = QTreeWidgetItem(["主机"])
        # icon = QIcon()
        # icon.addPixmap(QPixmap("img/主机记录.png"), QIcon.Mode.Normal, QIcon.State.Off)
        # itemhost.setIcon(0, icon)
        # self._ui.homeui.infoList.insertTopLevelItem(0, itemhost)
        # print("hosts")
        # for host in self.hosts:
        #     item = QTreeWidgetItem([host.name])
        #     itemhost.addChild(item)
        # itemjob = QTreeWidgetItem(["任务"])
        # icon = QIcon()
        # icon.addPixmap(QPixmap("img/任务进程.png"), QIcon.Mode.Normal, QIcon.State.Off)
        # itemjob.setIcon(0, icon)
        # self._ui.homeui.infoList.insertTopLevelItem(1, itemjob)
        # for job in self.jobs:
        #     item = QTreeWidgetItem([job.name])
        #     itemjob.addChild(item)
        # itemfault = QTreeWidgetItem(["故障"])
        # icon = QIcon()
        # icon.addPixmap(QPixmap("img/识别错误.png"), QIcon.Mode.Normal, QIcon.State.Off)
        # itemfault.setIcon(0, icon)
        # self._ui.homeui.infoList.insertTopLevelItem(2, itemfault)
        # for fault in self.faults:
        #     item = QTreeWidgetItem([fault.name])
        #     itemfault.addChild(item)
        
        # # 如果在侧边栏添加了新的仿真类别（交换机之类的），记得修改数量
        # self._ui.homeui.infoList.setColumnCount(3)
        return
        


    def _showInfo(self):
        # print("show info")
        # if_root = False
        # #获取点击item所属根节点的名称（如无根节点则返回自身）
        # self.nowClect = self._ui.homeui.infoList.currentItem().parent()
        # if self.nowClect is None:
        #     if_root = True
        #     self.nowClect = self._ui.homeui.infoList.currentItem()
        # print(self.nowClect.text(0))
        # if if_root:
        #     return
        # if self.nowClect.text(0) == '主机':
        #     host = sysSim.hosts[self._ui.homeui.infoList.currentItem().text(0)]
        #     self._initHostInfo(host)
        # elif self.nowClect.text(0) == '任务':
        #     job = sysSim.jobs[self._ui.homeui.infoList.currentItem().text(0)]
        #     self.__initJobInfo(job)
        # elif self.nowClect.text(0) == '故障':
        #     fault = sysSim.faults[self._ui.homeui.infoList.currentItem().text(0)]
        #     self._initFaultInfo(fault)
        return


    def _add(self):
        # print("add aa")
        # if self.nowClect is None:
        #     return
        # print("add")
        # if self.nowClect.text(0) == '主机':
        #     r = random.randint(0, 10000)
        #     name = "host" + f"_{r}"
        #     while name in sysSim.hosts:
        #         r = random.randint(0, 10000)
        #         name = "host" + f"_{r}"
        #     item = QTreeWidgetItem([name])
        #     item.setFlags(item.flags())
        #     self.nowClect.addChild(item)
        #     self._ui.homeui.infoList.setCurrentItem(item)
        #     new_host = HostInfo(name, [], [CPUInfo(2, 1000)], 4)
        #     sysSim.hosts[name] = new_host
        #     self._initHostInfo(new_host)
        # elif self.nowClect.text(0) == '任务':
        #     r = random.randint(0, 10000)
        #     name = "job" + f"_{r}"
        #     while name in sysSim.jobs:
        #         r = random.randint(0, 10000)
        #         name = "job" + f"_{r}"
        #     item = QTreeWidgetItem([name])
        #     item.setFlags(item.flags())
        #     self.nowClect.addChild(item)
        #     self._ui.homeui.infoList.setCurrentItem(item)
        #     new_job = JobInfo(name, 10, CPUTaskInfo(100, 1, 1000))
        #     sysSim.jobs[name] = new_job
        #     self.__initJobInfo(new_job)
        # elif self.nowClect.text(0) == '故障':
        #     r = random.randint(0, 10000)
        #     name = "fault" + f"_{r}"
        #     while name in sysSim.faults:
        #         r = random.randint(0, 10000)
        #         name = "fault" + f"_{r}"
        #     item = QTreeWidgetItem([name])
        #     item.setFlags(item.flags())
        #     self.nowClect.addChild(item)
        #     self._ui.homeui.infoList.setCurrentItem(item)
        #     new_fault = FaultGenerator("Normal", 10, 10)
        #     if len(sysSim.hosts) > 0:
        #         new_fault.setAim(list(sysSim.hosts.keys())[0])
        #     new_fault.setName(name)
        #     new_fault.setHardware("CPU")
        #     sysSim.faults[name] = new_fault
        #     self._initFaultInfo(new_fault)
        return


    def _applyHost(self):
        # print("apply host")
        # if self.nowHost is None:
        #     return
        # print(self.hostInfoPage.corenum.text() + "AAA")
        # if self.hostInfoPage.hostName.text() == "":
        #     QMessageBox.information(self, "", "主机名不能为空")
        #     self._initHostInfo(self.nowHost)
        #     return
        # if self.hostInfoPage.hostName.text() in sysSim.hosts and self.hostInfoPage.hostName.text() != self.nowHost.name:
        #     QMessageBox.information(self, "", "主机名重复")
        #     self._initHostInfo(self.nowHost)
        #     return
        # if self.hostInfoPage.ram.text() == "" or int(self.hostInfoPage.ram.value()) == 0:
        #     QMessageBox.information(self, "", "主机内存不能为0")
        #     self._initHostInfo(self.nowHost)
        #     return
        # if self.hostInfoPage.cpunum.text() == "" or int(self.hostInfoPage.cpunum.value()) == 0:
        #     print("asa")
        #     QMessageBox.information(self, "", "主机CPU数不能为0")
        #     self._initHostInfo(self.nowHost)
        #     return
        # if self.hostInfoPage.corenum.text() == "" or int(self.hostInfoPage.corenum.value()) == 0:
        #     QMessageBox.information(self, "", "主机CPU核数不能为0")
        #     self._initHostInfo(self.nowHost)
        #     return
        # if self.hostInfoPage.cpuflops.text() == "" or float(self.hostInfoPage.cpuflops.text()) == 0.0:
        #     QMessageBox.information(self, "", "主机核FLOPs不能为0")
        #     self._initHostInfo(self.nowHost)
        #     return
        # name_before = self.nowHost.name
        # self.nowHost.name = self.hostInfoPage.hostName.text()
        # self.nowHost.ram = self.hostInfoPage.ram.value()
        # cpunum = self.hostInfoPage.cpunum.value()
        # cpucore = self.hostInfoPage.corenum.value()
        # cpuflops = self.hostInfoPage.cpuflops.text()
        # self.nowHost.cpu_infos = []
        # for i in range(cpunum):
        #     self.nowHost.cpu_infos.append(CPUInfo(cpucore, cpuflops))
        # self.nowHost.video_card_infos = []
        # # 更新GPU
        # if self.gpu_num > 0:
        #     self.nowHost.video_card_infos = []
        #     gpus = []
        #     for i in range(self.hostInfoPage.gputable.rowCount() - 1):
        #         n = i + 1
        #         n = n.__str__()
        #         if int(self.hostInfoPage.gputable.item(i + 1, 1).text()) == 0:
        #             QMessageBox.information(self, "", "第" + n + "个GPU的核心数不能为0")
        #             continue
        #         if int(self.hostInfoPage.gputable.item(i + 1, 2).text()) == 0:
        #             QMessageBox.information(self, "", "第" + n + "个GPU的每SM核心数不能为0")
        #             continue
        #         if int(self.hostInfoPage.gputable.item(i + 1, 3).text()) == 0:
        #             QMessageBox.information(self, "", "第" + n + "个GPU的SM最大线程块数不能为0")
        #             continue
        #         if int(self.hostInfoPage.gputable.item(i + 1, 4).text()) == 0:
        #             QMessageBox.information(self, "", "第" + n + "个GPU的核心FLOPs不能为0")
        #             continue
        #         if int(self.hostInfoPage.gputable.item(i + 1, 5).text()) == 0:
        #             QMessageBox.information(self, "", "第" + n + "个GPU的显存不能为0")
        #             continue
        #         gpu = GPUInfo(int(self.hostInfoPage.gputable.item(i + 1, 1).text()), (int)(self.hostInfoPage.gputable.item(i + 1, 2).text()), (int)(self.hostInfoPage.gputable.item(i+ 1, 3).text()), (int)(self.hostInfoPage.gputable.item(i+1, 5).text()), (int)(self.hostInfoPage.gputable.item(i+1, 4).text()))
        #         gpus.append(gpu)
        #     if len(gpus) > 0:
        #         videoCardInfo = VideoCardInfo(gpus)
        #         if (int)(self.hostInfoPage.pcie.value()) == 0:
        #             QMessageBox.information(self, "", "PCIe带宽不能为0")
        #             return
        #         videoCardInfo.pcie_bw = (int)(self.hostInfoPage.pcie.value()) 
        #         print("apply: " + videoCardInfo.pcie_bw.__str__())
        #         self.nowHost.video_card_infos.append(videoCardInfo)
        # self.nowHost.print()
        # sysSim.hosts.pop(name_before)
        # sysSim.hosts[self.nowHost.name] = self.nowHost
        # self._initHostInfo(self.nowHost)
        # # 更新树
        # for i in range(self.nowClect.childCount()):
        #     if self.nowClect.child(i).text(0) == name_before:
        #         self.nowClect.child(i).setText(0, self.nowHost.name)
        #         break
        return
        
    def _applyJob(self):
        # print("apply job")
        # if self.nowJob is None:
        #     return
        # if self.jobInfoPage.jobName.text() == "":
        #     QMessageBox.information(self, "", "任务名不能为空")
        #     self.__initJobInfo(self.nowJob)
        #     return
        # if self.jobInfoPage.jobName.text() in sysSim.jobs and self.jobInfoPage.jobName.text() != self.nowJob.name:
        #     QMessageBox.information(self, "", "任务名重复")
        #     self.__initJobInfo(self.nowJob)
        #     return
        # if self.jobInfoPage.ram.text() == "" or int(self.jobInfoPage.ram.text()) == 0:
        #     QMessageBox.information(self, "", "任务请求内存不能为0")
        #     self.__initJobInfo(self.nowJob)
        #     return
        # if self.jobInfoPage.corenum.text() == "" or int(self.jobInfoPage.corenum.text()) == 0:
        #     QMessageBox.information(self, "", "任务请求CPU核数不能为0")
        #     self.__initJobInfo(self.nowJob)
        #     return
        # if self.jobInfoPage.ram.text() == "" or int(self.jobInfoPage.ram.text()) == 0:
        #     QMessageBox.information(self, "", "任务CPU部分计算量不能为0")
        #     self.__initJobInfo(self.nowJob)
        #     return
        # if self.jobInfoPage.period.text() == "":
        #     QMessageBox.information(self, "", "任务周期不能为空")
        #     self.__initJobInfo(self.nowJob)
        #     return
        # name_before = self.nowJob.name
        # self.nowJob.name = self.jobInfoPage.jobName.text()
        # self.nowJob.cpu_task.ram = self.jobInfoPage.ram.text()
        # self.nowJob.period = self.jobInfoPage.period.text()
        # self.nowJob.cpu_task.pes_number = self.jobInfoPage.corenum.value()
        # self.nowJob.cpu_task.length = self.jobInfoPage.cpuflops.text()
        # self.nowJob.gpu_task = None
        # print(self.jobInfoPage.host.currentText())
        # if self.jobInfoPage.host.currentText() != "不指定":
        #     self.nowJob.host = self.jobInfoPage.host.currentText()
        # else:
        #     self.nowJob.host = ""
        # if self.kernel_num > 0:
        #     request_gddram_total = 0
        #     task_input_size_total = 0
        #     task_output_size_total = 0
        #     kernels = []
        #     for i in range(self.jobInfoPage.gputable.rowCount() - 1):
        #         n = i + 1
        #         n = n.__str__()
        #         if int(self.jobInfoPage.gputable.item(i + 1, 1).text()) == 0:
        #             QMessageBox.information(self, "", "第" + n + "个内核的线程块数不能为0")
        #             continue
        #         if int(self.jobInfoPage.gputable.item(i + 1, 2).text()) == 0:
        #             QMessageBox.information(self, "", "第" + n + "个内核的每线程块线程数不能为0")
        #             continue
        #         if int(self.jobInfoPage.gputable.item(i + 1, 3).text()) == 0:
        #             QMessageBox.information(self, "", "第" + n + "个内核的每线程FLOPS不能为0")
        #             continue
        #         request_gddram_total += int(self.jobInfoPage.gputable.item(i + 1, 4).text())
        #         task_input_size_total += int(self.jobInfoPage.gputable.item(i + 1, 5).text())
        #         task_output_size_total += int(self.jobInfoPage.gputable.item(i + 1, 6).text())
        #         kernel = GPUTaskInfo.Kernel(int(self.jobInfoPage.gputable.item(i + 1, 1).text()), int(self.jobInfoPage.gputable.item(i + 1, 2).text()), int(self.jobInfoPage.gputable.item(i + 1, 3).text()))
        #         kernels.append(kernel)
        #     self.nowJob.gpu_task = GPUTaskInfo(kernels, request_gddram_total, task_input_size_total, task_output_size_total)
        # self.__initJobInfo(self.nowJob)
        # sysSim.jobs.pop(name_before)
        # sysSim.jobs[self.nowJob.name] = self.nowJob
        # self.nowJob.print()
        # # 更新树
        # for i in range(self.nowClect.childCount()):
        #     if self.nowClect.child(i).text(0) == name_before:
        #         self.nowClect.child(i).setText(0, self.nowJob.name)
        #         break
        return

    def _applyFault(self):
        # print("apply fault")
        # if self.nowFault is None:
        #     return
        # if self.faultInfoPage.name.text() == "":
        #     QMessageBox.information(self, "", "错误模型名不能为空")
        #     self._initFaultInfo(self.nowFault)
        #     return
        # if self.faultInfoPage.name.text() in sysSim.faults and self.faultInfoPage.name.text() != self.nowFault.name:
        #     QMessageBox.information(self, "", "错误模型名重复")
        #     self._initFaultInfo(self.nowFault)
        #     return
        # if self.faultInfoPage.time1.text() == "":
        #     QMessageBox.information(self, "", "平均无故障时间不能为空")
        #     self._initFaultInfo(self.nowFault)
        #     return
        # if self.faultInfoPage.time2.text() == "":
        #     QMessageBox.information(self, "", "平均故障修复时间不能为空")
        #     self._initFaultInfo(self.nowFault)
        #     return
        # if (int)(self.faultInfoPage.time1.text()) == 0:
        #     QMessageBox.information(self, "", "平均无故障时间不能为0")
        #     self._initFaultInfo(self.nowFault)
        #     return
        # if (int)(self.faultInfoPage.time2.text()) == 0:
        #     QMessageBox.information(self, "", "平均故障修复时间不能为0")
        #     self._initFaultInfo(self.nowFault)
        #     return
        # name_before = self.nowFault.name
        # newFault = FaultGenerator(tranFromC2E(self.faultInfoPage.type.currentText()), (float)(self.faultInfoPage.time1.text()), (float)(self.faultInfoPage.time2.text()))
        # newFault.setAim(self.faultInfoPage.aim.currentText())
        # newFault.setName(self.faultInfoPage.name.text())
        # if self.faultInfoPage.hardware.currentText() == "CPU":
        #     newFault.setHardware("CPU")
        # elif self.faultInfoPage.hardware.currentText() == "GPU":
        #     newFault.setHardware("gpu")
        # else:
        #     newFault.setHardware("ram")
        # newFault.print()
        # sysSim.faults.pop(name_before)
        # sysSim.faults[newFault.name] = newFault
        # self.nowFault = newFault
        # newFault.print()
        # self._initFaultInfo(newFault)
        # # 更新树
        # for i in range(self.nowClect.childCount()):
        #     if self.nowClect.child(i).text(0) == name_before:
        #         self.nowClect.child(i).setText(0, self.nowFault.name)
        #         break
        return

    def _initHostInfo(self, host: HostInfo, ifTrueHost=True):
        # self.gpu_num = 0
        # self.cpushow.setChart(QChart())
        # self.ramshow.setChart(QChart())
        # self.gpushow.setChart(QChart())
        # if ifTrueHost:
        #     self.nowHost = host
        # else:
        #     self.nowHost = None
        # if ifTrueHost and os.path.isdir(project.projectPath + "/OutputFiles") and os.path.isfile(project.projectPath + "/OutputFiles/hostUtils.xml"):
        #     path = project.projectPath + "/OutputFiles/hostUtils.xml"
        #     if os.path.exists(path):
        #         xmlParser = XmlParser(path)
        #         self.cluster_result = xmlParser.parseHostRecord()
        #         painter = Painter(self.cluster_result, [], [])
        #         chartCPU = painter.plotHostCPUUtilization(host.name, -1, float("inf"))
        #         self.cpushow.setChart(chartCPU)
        #         chartRam = painter.plotHostRamUtilization(host.name, -1, float("inf"))
        #         self.ramshow.setChart(chartRam)
        #         chartGPU = painter.plotGpuUtilization(host.name, -1, -1, float("inf"))
        #         self.gpushow.setChart(chartGPU)
        # self.hostInfoPage.hostName.setText(host.name)
        # self.hostInfoPage.ram.setValue(host.ram)
        # cpunum = len(host.cpu_infos)
        # cpucore = host.cpu_infos[0].cores
        # self.hostInfoPage.corenum.setValue(cpucore)
        # self.hostInfoPage.cpunum.setValue(cpunum)
        # self.hostInfoPage.cpuflops.setText(str(host.cpu_infos[0].mips))
        # # 设置正则表达式为运行2位小鼠数
        # reg_ex =  QRegularExpression("^([0-9]{1,}[.]{0,1}[0-9]{0,2})$")
        # validator = QRegularExpressionValidator(reg_ex, self.hostInfoPage.cpuflops)
        # self.hostInfoPage.cpuflops.setValidator(validator)
        # self._ui.homeui.tabWidget.setCurrentIndex(0)
        # if host.video_card_infos != []:
        #     print(host.video_card_infos[0].pcie_bw)
        #     self.hostInfoPage.pcie.setValue(host.video_card_infos[0].pcie_bw)
        #     gpu_num = len(host.video_card_infos[0].gpu_infos)
        #     if gpu_num > 0:
        #         self.gpu_num = gpu_num
        #         self.initGpuTable(gpu_num, host.video_card_infos[0].gpu_infos)
        #     else:
        #         self.gpu_num = 0
        #         self.initGpuTable(0, [])
        # else:
        #     self.gpu_num = 0
        #     self.initGpuTable(0, [])
        return
                
    def initGpuTable(self, gpu_num, gpu_infos):    
        # f = QFont()
        # f.setPointSize(10)
        # self.hostInfoPage.gputable.setFont(f)
        # delegate = NumericDelegate(self.hostInfoPage.gputable)
        # self.hostInfoPage.gputable.setItemDelegate(delegate)
        # self.hostInfoPage.gputable.setColumnCount(7)
        # self.hostInfoPage.gputable.setRowCount(gpu_num + 1)
        # # 设置不可见
        # self.hostInfoPage.gputable.verticalHeader().setVisible(False)
        # self.hostInfoPage.gputable.horizontalHeader().setVisible(False)
        # i = 0
        # # self.hostInfoPage.gputable.setItem(i, 0, QTableWidgetItem("GPU ID"))
        # # self.hostInfoPage.gputable.setItem(i, 1, QTableWidgetItem("GPU 核心数"))
        # # self.hostInfoPage.gputable.setItem(i, 2, QTableWidgetItem("GPU 每流处理器核心数"))
        # # self.hostInfoPage.gputable.setItem(i, 3, QTableWidgetItem("GPU 每流处理器最大线程块数"))
        # # self.hostInfoPage.gputable.setItem(i, 4, QTableWidgetItem("GPU 核心FLOPs"))
        # # self.hostInfoPage.gputable.setItem(i, 5, QTableWidgetItem("GPU 显存"))
        # # 第一行背景设为灰色，信息如上所示
        # item1 = QTableWidgetItem("GPU ID")
        # item1.setBackground(QColor(192, 192, 192))
        # self.hostInfoPage.gputable.setItem(i, 0, item1)
        # item2 = QTableWidgetItem("核心数")
        # item2.setBackground(QColor(192, 192, 192))
        # self.hostInfoPage.gputable.setItem(i, 1, item2)
        # item3 = QTableWidgetItem("SM核心数")
        # item3.setBackground(QColor(192, 192, 192))
        # self.hostInfoPage.gputable.setItem(i, 2, item3)
        # item4 = QTableWidgetItem("SM最大线程块")
        # item4.setBackground(QColor(192, 192, 192))
        # self.hostInfoPage.gputable.setItem(i, 3, item4)
        # item5 = QTableWidgetItem("TFLOPS")
        # item5.setBackground(QColor(192, 192, 192))
        # self.hostInfoPage.gputable.setItem(i, 4, item5)
        # item6 = QTableWidgetItem("显存(GB)")
        # item6.setBackground(QColor(192, 192, 192))
        # self.hostInfoPage.gputable.setItem(i, 5, item6)

        # for gpu_info in gpu_infos:
        #     i += 1
        #     self.hostInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
        #     self.hostInfoPage.gputable.setItem(i, 1, QTableWidgetItem(str(gpu_info.cores)))
        #     self.hostInfoPage.gputable.setItem(i, 2, QTableWidgetItem(str(gpu_info.core_per_sm)))
        #     self.hostInfoPage.gputable.setItem(i, 3, QTableWidgetItem(str(gpu_info.max_block_per_sm))
        #     )
        #     self.hostInfoPage.gputable.setItem(i, 4, QTableWidgetItem(str(gpu_info.flops_per_core)))
        #     self.hostInfoPage.gputable.setItem(i, 5, QTableWidgetItem(str(gpu_info.gddram)))
        #     del_gpu = QPushButton()
        #     del_gpu.setText("删除")
        #     del_gpu.clicked.connect(self._delGpu)
        #     self.hostInfoPage.gputable.setCellWidget(i, 6, del_gpu)
        return

    def _delGpu(self):
        # print("del gpu")
        # row = self.hostInfoPage.gputable.currentRow()
        # self.hostInfoPage.gputable.removeRow(row)
        # self.gpu_num -= 1
        # for i in range(row, self.gpu_num + 1):
        #     self.hostInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
        return

    def _addGpu(self):
        # if self.nowHost is None:
        #     return
        # self.gpu_num += 1
        # self.hostInfoPage.gputable.setRowCount(self.gpu_num + 1)
        # i = self.gpu_num
        # if self.gpu_num == 1:
        #     self.hostInfoPage.gputable.setColumnCount(7)
        #     item1 = QTableWidgetItem("GPU ID")
        #     item1.setBackground(QColor(192, 192, 192))
        #     self.hostInfoPage.gputable.setItem(0, 0, item1)
        #     item2 = QTableWidgetItem("核心数")
        #     item2.setBackground(QColor(192, 192, 192))
        #     self.hostInfoPage.gputable.setItem(0, 1, item2)
        #     item3 = QTableWidgetItem("SM核心数")
        #     item3.setBackground(QColor(192, 192, 192))
        #     self.hostInfoPage.gputable.setItem(0, 2, item3)
        #     item4 = QTableWidgetItem("SM最大线程块")
        #     item4.setBackground(QColor(192, 192, 192))
        #     self.hostInfoPage.gputable.setItem(0, 3, item4)
        #     item5 = QTableWidgetItem("TFLOPS")
        #     item5.setBackground(QColor(192, 192, 192))
        #     self.hostInfoPage.gputable.setItem(0, 4, item5)
        #     item6 = QTableWidgetItem("显存(GB)")
        #     item6.setBackground(QColor(192, 192, 192))
        #     self.hostInfoPage.gputable.setItem(0, 5, item6)

        # self.hostInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
        # self.hostInfoPage.gputable.setItem(i, 1, QTableWidgetItem("0"))
        # self.hostInfoPage.gputable.setItem(i, 2, QTableWidgetItem("0"))
        # self.hostInfoPage.gputable.setItem(i, 3, QTableWidgetItem("0"))
        # self.hostInfoPage.gputable.setItem(i, 4, QTableWidgetItem("0"))
        # self.hostInfoPage.gputable.setItem(i, 5, QTableWidgetItem("0"))
        # del_gpu = QPushButton()
        # del_gpu.setText("删除")
        # del_gpu.clicked.connect(self._delGpu)
        # self.hostInfoPage.gputable.setCellWidget(i, 6, del_gpu)
        return

    def __initJobInfo(self, job: JobInfo, ifTrueJob=True):
        # if ifTrueJob:
        #     self.nowJob = job
        # else:
        #     self.nowJob = None
        # if ifTrueJob and os.path.isdir(project.projectPath + "/OutputFiles") and os.path.isfile(project.projectPath + "/OutputFiles/jobRun.xml"):
        #     path = project.projectPath + "/OutputFiles/jobRun.xml"
        #     if os.path.exists(path):
        #         xmlParser = XmlParser(path)
        #         self.job_result = xmlParser.parseJobRecord()
        #         painter = Painter([], self.job_result, [])
        #         chart = painter.plotJobDuration(job.name)
        #         self.jobInfoPage.showjob.setChart(chart)
        # self.jobInfoPage.jobName.setText(job.name)
        # self.jobInfoPage.ram.setText(str(job.cpu_task.ram))
        # reg_ex =  QRegularExpression("[0-9]+")
        # validator = QRegularExpressionValidator(reg_ex, self.jobInfoPage.ram)
        # self.jobInfoPage.ram.setValidator(validator)
        # self.jobInfoPage.period.setText(str(job.period))
        # reg_ex =  QRegularExpression("[0-9]+")
        # validator = QRegularExpressionValidator(reg_ex, self.jobInfoPage.period)
        # self.jobInfoPage.period.setValidator(validator)
        # self.jobInfoPage.corenum.setValue(job.cpu_task.pes_number)
        # self.jobInfoPage.cpuflops.setText(str(job.cpu_task.length))
        # reg_ex =  QRegularExpression("[0-9]+")
        # validator = QRegularExpressionValidator(reg_ex, self.jobInfoPage.cpuflops)
        # self.jobInfoPage.cpuflops.setValidator(validator)
        # if job.gpu_task is not None:
        #     print("gpu task")
        #     self.kernel_num = len(job.gpu_task.kernels)
        #     self._initKernelTable(len(job.gpu_task.kernels), job.gpu_task)
        # else:
        #     print("no gpu task")
        #     self.kernel_num = 0
        #     self._initKernelTable(0, None)
        # self.jobInfoPage.host.clear()
        # self.jobInfoPage.host.addItem("不指定")
        # for(host_name, host) in sysSim.hosts.items():
        #     self.jobInfoPage.host.addItem(host_name)
        # print(job.host)
        # print("===")
        # if job.host != "":
        #     self.jobInfoPage.host.setCurrentText(job.host)
        # else:
        #     self.jobInfoPage.host.setCurrentText("不指定")
        # self._ui.homeui.tabWidget.setCurrentIndex(1)
        return

    def _initKernelTable(self, kernel_num, gpu_task):
        # delegate = NumericDelegate(self.jobInfoPage.gputable)
        # self.jobInfoPage.gputable.setItemDelegate(delegate)
        # self.jobInfoPage.gputable.setColumnCount(8)
        # self.jobInfoPage.gputable.setRowCount(kernel_num + 1)
        # # 设置不可见
        # self.jobInfoPage.gputable.verticalHeader().setVisible(False)
        # self.jobInfoPage.gputable.horizontalHeader().setVisible(False)
        # i = 0
        # item1 = QTableWidgetItem("内核 ID")
        # item1.setBackground(QColor(192, 192, 192))
        # self.jobInfoPage.gputable.setItem(i, 0, item1)
        # item2 = QTableWidgetItem("线程块数")
        # item2.setBackground(QColor(192, 192, 192))
        # self.jobInfoPage.gputable.setItem(i, 1, item2)
        # item3 = QTableWidgetItem("线程数")
        # item3.setBackground(QColor(192, 192, 192))
        # self.jobInfoPage.gputable.setItem(i, 2, item3)
        # item4 = QTableWidgetItem("TFLOP")
        # item4.setBackground(QColor(192, 192, 192))
        # self.jobInfoPage.gputable.setItem(i, 3, item4)
        # item5 = QTableWidgetItem("需求显存(MB)")    
        # item5.setBackground(QColor(192, 192, 192))
        # self.jobInfoPage.gputable.setItem(i, 4, item5)
        # item6 = QTableWidgetItem("输入(MB)")
        # item6.setBackground(QColor(192, 192, 192))
        # self.jobInfoPage.gputable.setItem(i, 5, item6)
        # item7 = QTableWidgetItem("输出(MB)")
        # item7.setBackground(QColor(192, 192, 192))
        # self.jobInfoPage.gputable.setItem(i, 6, item7)
        # i = 0
        # if gpu_task is not None:
        #     for kernel_info in gpu_task.kernels:
        #         i += 1
        #         self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
        #         self.jobInfoPage.gputable.setItem(i, 1, QTableWidgetItem(str(kernel_info.block_num)))
        #         self.jobInfoPage.gputable.setItem(i, 2, QTableWidgetItem(str(kernel_info.thread_num)))
        #         self.jobInfoPage.gputable.setItem(i, 3, QTableWidgetItem(str(kernel_info.thread_length)))
        #         self.jobInfoPage.gputable.setItem(i, 4, QTableWidgetItem(str(gpu_task.requested_gddram_size)))
        #         self.jobInfoPage.gputable.setItem(i, 5, QTableWidgetItem(str(gpu_task.task_input_size)))
        #         self.jobInfoPage.gputable.setItem(i, 6, QTableWidgetItem(str(gpu_task.task_output_size)))
        #         del_kernel = QPushButton()
        #         del_kernel.setText("删除")
        #         del_kernel.clicked.connect(self._delKernel)
        #         self.jobInfoPage.gputable.setCellWidget(i, 7, del_kernel)
        return
        

    def _delKernel(self):
        # print("del kernel")
        # row = self.jobInfoPage.gputable.currentRow()
        # self.jobInfoPage.gputable.removeRow(row)
        # self.kernel_num -= 1
        # for i in range(row, self.kernel_num + 1):
        #     self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
        return

    def _addKernel(self):
        # if self.nowJob is None:
        #     return
        # self.kernel_num += 1
        # print("add kernel: " + str(self.kernel_num))
        # self.jobInfoPage.gputable.setRowCount(self.kernel_num + 1)
        # i = self.kernel_num
        # if self.kernel_num == 1:
        #     self.jobInfoPage.gputable.setColumnCount(8)
        #     item1 = QTableWidgetItem("内核 ID")
        #     item1.setBackground(QColor(192, 192, 192))
        #     self.jobInfoPage.gputable.setItem(0, 0, item1)
        #     item2 = QTableWidgetItem("线程块数")
        #     item2.setBackground(QColor(192, 192, 192))
        #     self.jobInfoPage.gputable.setItem(0, 1, item2)
        #     item3 = QTableWidgetItem("线程数")
        #     item3.setBackground(QColor(192, 192, 192))
        #     self.jobInfoPage.gputable.setItem(0, 2, item3)
        #     item4 = QTableWidgetItem("TFLOP")
        #     item4.setBackground(QColor(192, 192, 192))
        #     self.jobInfoPage.gputable.setItem(0, 3, item4)
        #     item5 = QTableWidgetItem("需求显存(MB)")    
        #     item5.setBackground(QColor(192, 192, 192))
        #     self.jobInfoPage.gputable.setItem(0, 4, item5)
        #     item6 = QTableWidgetItem("输入(MB)")
        #     item6.setBackground(QColor(192, 192, 192))
        #     self.jobInfoPage.gputable.setItem(0, 5, item6)
        #     item7 = QTableWidgetItem("输出(MB)")
        #     item7.setBackground(QColor(192, 192, 192))
        #     self.jobInfoPage.gputable.setItem(0, 6, item7)
            

        # self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
        # self.jobInfoPage.gputable.setItem(i, 1, QTableWidgetItem("0"))
        # self.jobInfoPage.gputable.setItem(i, 2, QTableWidgetItem("0"))
        # self.jobInfoPage.gputable.setItem(i, 3, QTableWidgetItem("0"))
        # self.jobInfoPage.gputable.setItem(i, 4, QTableWidgetItem("0"))
        # self.jobInfoPage.gputable.setItem(i, 5, QTableWidgetItem("0"))
        # self.jobInfoPage.gputable.setItem(i, 6, QTableWidgetItem("0"))
        # del_kernel = QPushButton()
        # del_kernel.setText("删除")
        # del_kernel.clicked.connect(self._delKernel)
        # self.jobInfoPage.gputable.setCellWidget(i, 7, del_kernel)
        return


    def _initFaultInfo(self, fault: FaultGenerator, ifTrueFault=True):
        # self.showFaultInject.setChart(QChart())
        # self.showFaultInject2.setChart(QChart())
        # self.faultRecordTable.setRowCount(0)
        # if ifTrueFault:
        #     print(fault.mttf_type + " 是这个")
        #     self.nowFault = fault
        #     self.faultInfoPage.aim.clear()
        #     self.faultInfoPage.aim.addItems(sysSim.hosts.keys())
        #     self.faultInfoPage.name.setText(fault.name)
        #     self.faultInfoPage.aim.setCurrentText(fault.aim)
        #     self.faultInfoPage.type.setCurrentText(tranFromE2C(fault.mttf_type))
        #     print(tranFromE2C(fault.mttf_type))
        #     self.faultInfoPage.time1.setText(str((int)(fault.mttf_scale)))
        #     regular_ex = QRegularExpression("[0-9]+")
        #     validator = QRegularExpressionValidator(regular_ex, self.faultInfoPage.time1)
        #     self.faultInfoPage.time1.setValidator(validator)
        #     self.faultInfoPage.time2.setText(str((int)(fault.mttr_scale)))
        #     regular_ex = QRegularExpression("[0-9]+")
        #     validator = QRegularExpressionValidator(regular_ex, self.faultInfoPage.time2)
        #     self.faultInfoPage.time2.setValidator(validator)
        #     self._ui.homeui.tabWidget.setCurrentIndex(2)
        #     if fault.mttf_type == "Normal":
        #         self.showFaultInject.setChart(self.__getNormalLine(fault.mttf_scale))
        #         self.showFaultInject2.setChart(self.__getNormalLine(fault.mttr_scale))
        #     elif fault.mttf_type == "LogNormal":
        #         self.showFaultInject.setChart(self.__getLogNormalLine(fault.mttf_scale))
        #         self.showFaultInject2.setChart(self.__getLogNormalLine(fault.mttr_scale))
        #     elif fault.mttf_type == "Weibull":
        #         self.showFaultInject.setChart(self.__getWeiBullLine(fault.mttf_scale))
        #         self.showFaultInject2.setChart(self.__getWeiBullLine(fault.mttr_scale))
        #     elif fault.mttf_type == "Gamma":
        #         self.showFaultInject.setChart(self.__getGammaLine(fault.mttf_scale))
        #         self.showFaultInject2.setChart(self.__getGammaLine(fault.mttr_scale))
        #     if fault.type == "CPU":
        #         self.faultInfoPage.hardware.setCurrentIndex(0)
        #     elif fault.type == "ram":
        #         self.faultInfoPage.hardware.setCurrentIndex(1)
        #      # 填充故障信息表格
        #     path = project.projectPath + "/OutputFiles/faultRecords.xml"
        #     print(path)
        #     if os.path.exists(path) and os.path.isdir(project.projectPath + "/OutputFiles") and os.path.isfile(project.projectPath + "/OutputFiles/faultRecords.xml"):
        #         print("exist")
        #         xmlParser = XmlParser(path)
        #         fault_results = xmlParser.parseFaultRecord()
        #         fault_num = len(fault_results)
        #         # 设置不可见
        #         self.faultRecordTable.verticalHeader().setVisible(False)
        #         self.faultRecordTable.horizontalHeader().setVisible(True)
        #         self.faultRecordTable.setColumnCount(5)
        #         self.faultRecordTable.setRowCount(fault_num)
        #         self.faultRecordTable.setHorizontalHeaderLabels(["时间", "故障对象", "类型", "恢复", "虚警"])
        #         i = 0
        #         for faultRecord in fault_results:
        #             self.faultRecordTable.setItem(i, 0, QTableWidgetItem(faultRecord.time))
        #             self.faultRecordTable.setItem(i, 1, QTableWidgetItem(faultRecord.object))
        #             self.faultRecordTable.setItem(i, 2, QTableWidgetItem(faultRecord.type))
        #             if(faultRecord.isSuccessRebuild == "True"):
        #                 self.faultRecordTable.setItem(i, 3, QTableWidgetItem("成功"))
        #             else:
        #                 self.faultRecordTable.setItem(i, 3, QTableWidgetItem("失败"))
        #             if(faultRecord.isFalseAlarm == "True"):
        #                 self.faultRecordTable.setItem(i, 4, QTableWidgetItem("是"))
        #             else:
        #                 self.faultRecordTable.setItem(i, 4, QTableWidgetItem("否"))
        #             i += 1
        # else:
        #     self.nowFault = None
        #     self.faultInfoPage.aim.clear()
        #     #self.faultInfoPage.aim.addItems(sysSim.hosts.keys())
        #     self.faultInfoPage.name.setText("")
        #     self.faultInfoPage.aim.setCurrentText("")
        #     self.faultInfoPage.type.setCurrentText("")
        #     self.faultInfoPage.time1.setText("")
        #     regular_ex = QRegularExpression("[0-9]+")
        #     validator = QRegularExpressionValidator(regular_ex, self.faultInfoPage.time1)
        #     self.faultInfoPage.time1.setValidator(validator)
        #     self.faultInfoPage.time2.setText("")
        #     regular_ex = QRegularExpression("[0-9]+")
        #     validator = QRegularExpressionValidator(regular_ex, self.faultInfoPage.time2)
        #     self.faultInfoPage.time2.setValidator(validator)
        #     self._ui.homeui.tabWidget.setCurrentIndex(2)
        #     #self.faultInfoPage.show.setChart(QChart())
        return

    def __getNormalLine(self, avg):
        print("get normal line")
        chart = QChart()
        rng = np.random.default_rng()
        data = rng.normal(avg, 1, 200000) 
        res_freq = stats.relfreq(data, numbins=100)
        pdf_value = res_freq.frequency
        x = res_freq.lowerlimit + np.linspace(0, res_freq.binsize * res_freq.frequency.size, res_freq.frequency.size)
        self.series=QLineSeries()
        self.series.setName("平均无故障时间分布")
        # 填充QLineSeries
        for i in range(len(x)):
                self.series.append(x[i],pdf_value[i])
        chart.addSeries(self.series)
        # 设置x坐标
        self.axis_x=QValueAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setLabelFormat("%.2f")
        self.axis_x.setTitleText("值(秒)")

        chart.addAxis(self.axis_x,Qt.AlignBottom) # 在表格中加入坐标，位置为底部
        self.series.attachAxis(self.axis_x) # 自动让QLineSeries贴附

        # 设置y坐标
        self.axis_y=QValueAxis()
        self.axis_y.setTickCount(5)
        self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setTitleText("概率")
        chart.addAxis(self.axis_y,Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)
        return chart


    def __getLogNormalLine(self, avg):
        print("get lognormal line")
        chart = QChart()
        rng = np.random.default_rng()
        data = rng.lognormal(avg, 1, 200000) 
        res_freq = stats.relfreq(data, numbins=100)
        pdf_value = res_freq.frequency
        x = res_freq.lowerlimit + np.linspace(0, res_freq.binsize * res_freq.frequency.size, res_freq.frequency.size)
        self.series=QLineSeries()
        self.series.setName("平均无故障时间分布")
        # 填充QLineSeries
        for i in range(len(x)):
                self.series.append(x[i],pdf_value[i])
        chart.addSeries(self.series)

        # 设置x坐标
        self.axis_x=QValueAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setLabelFormat("%.2f")
        self.axis_x.setTitleText("值(秒)")

        chart.addAxis(self.axis_x,Qt.AlignBottom) # 在表格中加入坐标，位置为底部
        self.series.attachAxis(self.axis_x)

        # 设置y坐标
        self.axis_y=QValueAxis()
        self.axis_y.setTickCount(5)
        self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setTitleText("概率")
        chart.addAxis(self.axis_y,Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        return chart

    def __getWeiBullLine(self, avg):
        print("get weibull line")
        chart = QChart()
        rng = np.random.default_rng()
        data = rng.weibull(avg, 200000) 
        res_freq = stats.relfreq(data, numbins=100)
        pdf_value = res_freq.frequency
        x = res_freq.lowerlimit + np.linspace(0, res_freq.binsize * res_freq.frequency.size, res_freq.frequency.size)
        self.series=QLineSeries()
        self.series.setName("平均无故障时间分布")
        # 填充QLineSeries
        for i in range(len(x)):
                self.series.append(x[i],pdf_value[i])
        chart.addSeries(self.series)

        # 设置x坐标
        self.axis_x=QValueAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setLabelFormat("%.2f")
        self.axis_x.setTitleText("值(秒)")

        chart.addAxis(self.axis_x,Qt.AlignBottom) # 在表格中加入坐标，位置为底部
        self.series.attachAxis(self.axis_x)
        
        # 设置y坐标
        self.axis_y=QValueAxis()
        self.axis_y.setTickCount(5)

        self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setTitleText("概率")
        chart.addAxis(self.axis_y,Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        return chart

    def __getGammaLine(self, avg):
        print("get gamma line")
        chart = QChart()
        rng = np.random.default_rng()
        data = rng.gamma(avg, 1, 200000) 
        res_freq = stats.relfreq(data, numbins=100)
        pdf_value = res_freq.frequency
        x = res_freq.lowerlimit + np.linspace(0, res_freq.binsize * res_freq.frequency.size, res_freq.frequency.size)
        self.series=QLineSeries()
        self.series.setName("平均无故障时间分布")
        # 填充QLineSeries
        for i in range(len(x)):
                self.series.append(x[i],pdf_value[i])
        chart.addSeries(self.series)

        # 设置x坐标
        self.axis_x=QValueAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setLabelFormat("%.2f")
        self.axis_x.setTitleText("值(秒)")

        chart.addAxis(self.axis_x,Qt.AlignBottom) # 在表格中加入坐标，位置为底部
        self.series.attachAxis(self.axis_x)

        # 设置y坐标
        self.axis_y=QValueAxis()
        self.axis_y.setTickCount(5)
        self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setTitleText("概率")
        chart.addAxis(self.axis_y,Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        return chart


       

    def _delete(self):
        # print("delete")
        # if self.nowClect is None:
        #     print("none")
        #     return
        # if self.nowClect.text(0) == '主机':
        #     sysSim.hosts.pop(self._ui.homeui.infoList.currentItem().text(0))
        #     self._ui.homeui.tabWidget.setCurrentIndex(0)
        #     self._initHostInfo(HostInfo("", [], [CPUInfo(0, 0)], 0), False)
        # elif self.nowClect.text(0) == '任务':
        #     sysSim.jobs.pop(self._ui.homeui.infoList.currentItem().text(0))
        #     self._ui.homeui.tabWidget.setCurrentIndex(1)
        #     self.__initJobInfo(JobInfo("", 0, CPUTaskInfo(0, 0, 0)), False)
        # elif self.nowClect.text(0) == '故障':
        #     sysSim.faults.pop(self._ui.homeui.infoList.currentItem().text(0))
        #     self._ui.homeui.tabWidget.setCurrentIndex(2)
        #     fault = FaultGenerator("正态分布", 0, 0)
        #     fault.setAim("")
        #     fault.setName("")
        #     fault.setHardware("CPU")
        #     self._initFaultInfo(FaultGenerator("正态分布", 0, 0), False)
        # self.nowClect.removeChild(self._ui.homeui.infoList.currentItem())
        return
    
    def _run(self):
        self._ui.central_window.centralWidget().setEnabled(False)
        # self._ui.action_enable.setEnabled(True)
        # self._ui.action_disable.setEnabled(False)
        hosts_json = json.dumps([host.__dict__ for host in sysSim.hosts.values()], indent=4, default=lambda o: o.__dict__)
        with open(project.projectPath + "/hosts.json", 'w') as write_f:
            write_f.write(hosts_json)
        jobs_json = json.dumps([job.__dict__ for job in sysSim.jobs.values()], indent=4, default=lambda o: o.__dict__)
        with open(project.projectPath + "/jobs.json",'w') as write_f:
            write_f.write(jobs_json)
        fault_json = json.dumps([fault.__dict__ for fault in sysSim.faults.values()], indent=4, default=lambda o: o.__dict__)
        with open(project.projectPath + "/faults.json", 'w') as write_f:
            write_f.write(fault_json)
        if sysSim.hosts == {}:
            QMessageBox.information(self, "", "未设置主机信息") 
            self._ui.central_window.centralWidget().setEnabled(True)
            return
        if sysSim.jobs == {}:
            QMessageBox.information(self, "", "未设置任务信息")
            self._ui.central_window.centralWidget().setEnabled(True)
            return
        execute = globaldata.targetPath[2] + " " + project.projectPath + "/OutputFiles " + project.projectPath + "/hosts.json " + project.projectPath + "/jobs.json " + project.projectPath + "/faults.json " + str(0) + " " + str(self.duration)
        print(execute)
        popen = subprocess.Popen(execute, shell=True, stdout=subprocess.PIPE,  universal_newlines=True, stderr=subprocess.STDOUT)
        out,err = popen.communicate()
        # print('std_out: ' + out)
        #将日志信息显示在文本框中
        self._ui.homeui.textEdit.setText(out)
        if "任务群总完成时间" in out:
            QMessageBox.information(self, "提示", "仿真完成")
        self._ui.central_window.centralWidget().setEnabled(True)
        os.popen(f"{globaldata.targetPath[3]} {project.projectPath} 1")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(sys.argv)
    # if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):  # Enable High DPI display with Qt5
    #     app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    # QDir.addSearchPath("icons", f"{get_project_root_path().as_posix()}/widget_gallery/ui/svg")
    win = JobSimQt()
    win.menuBar().setNativeMenuBar(False)
    app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    win.show()
    app.exec()
