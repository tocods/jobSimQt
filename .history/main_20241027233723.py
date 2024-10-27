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
import PySide6.QtWidgets
from qdarktheme.util import get_project_root_path
from main_ui import UI
from util.jobSim import sysSim, ParseUtil, HostInfo, CPUInfo, GPUInfo, VideoCardInfo, JobInfo, CPUTaskInfo, GPUTaskInfo, FaultGenerator, tranFromC2E, tranFromE2C
from jobSimPage import JobSimPage
from component.hostinfo import Ui_HostInfo
from component.jobinfo import Ui_JobInfo
from component.faultinfo import Ui_FaultInfo
from PySide6.QtCharts import QChart,QChartView,QLineSeries,QDateTimeAxis,QValueAxis, QPieSeries
from jobSimPainter import Painter, XmlParser
from util.table import NumericDelegate
from resultUtil import getAverageRunTime, getAverageRunTimeInHost, getThroughput

class JobSimQt(QMainWindow):
    def __init__(self, path) -> None:
        super().__init__()
        self.duration = 100
        project.projectPath = path
        self._initJsonFiles()
        # 取消标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.nowClect = None
        self._ui = UI()
        self._ui.setup_ui(self)

        # Signal
        self._ui.action_change_home.triggered.connect(self._change_page)
        self._ui.action_change_dock.triggered.connect(self._change_page)
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
        self._ui.homeui.infoList.setHeaderHidden(True)
        self.setGeometry(0, 0, screen_size.width() * 0.9, screen_size.height() * 0.9)
        self._ui.homeui.widget.setGeometry(0, 0, screen_size.width() * 0.8, screen_size.height() * 0.8)
        self._ui.resultui.layoutWidget.setGeometry(0, 0, screen_size.width() * 0.8, screen_size.height() * 0.8)
        self._initAll()
        self.initTreeView()
        self.setClicked()
        self.center()

    def center(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    @Slot()
    def _change_page(self) -> None:
        action_name = self.sender().text()
        self._ui.stack_widget.setCurrentIndex(0 if action_name == "运行仿真" else 1)

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

    def setClicked(self):
        self._ui.homeui.add.clicked.connect(self._add)
        self._ui.homeui.add.setIcon(QIcon("img/加.png"))
        self._ui.homeui.pushButton.clicked.connect(self._delete)
        self._ui.homeui.pushButton.setIcon(QIcon("img/减少.png"))
        self._ui.homeui.textEdit.setReadOnly(True)
        self._ui.homeui.run.clicked.connect(self._run)
        self._ui.homeui.infoList.clicked.connect(self._showInfo)

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
        self._initJsonFiles()
        self._initAll()
        self.initTreeView()
        self._ui.stack_widget.setCurrentIndex(0)
        self._ui.resultui.hostTabs.clear()
        self._ui.resultui.jobTabs.clear()
        self._ui.resultui.faultTabs.clear()
        self._ui.resultui.show.setChart(QChart())
        self._ui.resultui.showCPU.setChart(QChart())
        self._ui.resultui.showRam.setChart(QChart())
        self._ui.resultui.showGPU.setChart(QChart())
        self._ui.resultui.faultResultAnalysis.setChart(QChart())
        self._ui.resultui.jobResultAnalysis.setChart(QChart())

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
        print(self.hosts)
        for host in self.hosts:
            sysSim.hosts[host.name] = host
        path = project.projectPath + "/jobs.json"
        self.jobs = parser.parseJobs(path)
        for job in self.jobs:
            sysSim.jobs[job.name] = job
        path = project.projectPath + "/faults.json"
        self.faults = parser.parseFaults(path)
        for fault in self.faults:
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
        w.setGeometry(0, 0, screesize.width(), screesize.height())

        j = QWidget()
        self.jobInfoPage = Ui_JobInfo()
        self.jobInfoPage.setupUi(j)
        self.jobInfoPage.pushButton.setIcon(QIcon("img/加.png"))
        self.jobInfoPage.apply.clicked.connect(self._applyJob)
        self.jobInfoPage.pushButton.clicked.connect(self._addKernel)
        self._ui.homeui.tabWidget.addTab(j, "任务")
        j.setGeometry(0, 0, screesize.width(), screesize.height())

        f = QWidget()
        self.faultInfoPage = Ui_FaultInfo()
        self.faultInfoPage.setupUi(f)
        self.faultInfoPage.apply.clicked.connect(self._applyFault)
        self.show = QWidget()
        self.verticalLayout = QVBoxLayout()
        self.show
        self._ui.homeui.tabWidget.addTab(f, "故障")
        f.setGeometry(0, 0, screesize.width(), screesize.height())

        #self._initResult()


    def initTreeView(self):
        # 删除所有节点
        self._ui.homeui.infoList.clear()
        
        itemhost = QTreeWidgetItem(["主机"])
        icon = QIcon()
        icon.addPixmap(QPixmap("img/主机记录.png"), QIcon.Mode.Normal, QIcon.State.Off)
        itemhost.setIcon(0, icon)
        self._ui.homeui.infoList.insertTopLevelItem(0, itemhost)
        for host in self.hosts:
            item = QTreeWidgetItem([host.name])
            itemhost.addChild(item)
        itemjob = QTreeWidgetItem(["任务"])
        icon = QIcon()
        icon.addPixmap(QPixmap("img/任务进程.png"), QIcon.Mode.Normal, QIcon.State.Off)
        itemjob.setIcon(0, icon)
        self._ui.homeui.infoList.insertTopLevelItem(1, itemjob)
        for job in self.jobs:
            item = QTreeWidgetItem([job.name])
            itemjob.addChild(item)
        itemfault = QTreeWidgetItem(["故障"])
        icon = QIcon()
        icon.addPixmap(QPixmap("img/识别错误.png"), QIcon.Mode.Normal, QIcon.State.Off)
        itemfault.setIcon(0, icon)
        self._ui.homeui.infoList.insertTopLevelItem(2, itemfault)
        for fault in self.faults:
            item = QTreeWidgetItem([fault.name])
            itemfault.addChild(item)
        


    def _showInfo(self):
        print("show info")
        if_root = False
        #获取点击item所属根节点的名称（如无根节点则返回自身）
        self.nowClect = self._ui.homeui.infoList.currentItem().parent()
        if self.nowClect is None:
            if_root = True
            self.nowClect = self._ui.homeui.infoList.currentItem()
        print(self.nowClect.text(0))
        if if_root:
            return
        if self.nowClect.text(0) == '主机':
            host = sysSim.hosts[self._ui.homeui.infoList.currentItem().text(0)]
            self._initHostInfo(host)
        elif self.nowClect.text(0) == '任务':
            job = sysSim.jobs[self._ui.homeui.infoList.currentItem().text(0)]
            self.__initJobInfo(job)
        elif self.nowClect.text(0) == '故障':
            fault = sysSim.faults[self._ui.homeui.infoList.currentItem().text(0)]
            self._initFaultInfo(fault)


    def _add(self):
        print("add aa")
        if self.nowClect is None:
            return
        print("add")
        if self.nowClect.text(0) == '主机':
            r = random.randint(0, 10000)
            name = "host" + f"_{r}"
            while name in sysSim.hosts:
                r = random.randint(0, 10000)
                name = "host" + f"_{r}"
            item = QTreeWidgetItem([name])
            item.setFlags(item.flags())
            self.nowClect.addChild(item)
            self._ui.homeui.infoList.setCurrentItem(item)
            new_host = HostInfo(name, [], [CPUInfo(2, 1000)], 4)
            sysSim.hosts[name] = new_host
            self._initHostInfo(new_host)
        elif self.nowClect.text(0) == '任务':
            r = random.randint(0, 10000)
            name = "job" + f"_{r}"
            while name in sysSim.jobs:
                r = random.randint(0, 10000)
                name = "job" + f"_{r}"
            item = QTreeWidgetItem([name])
            item.setFlags(item.flags())
            self.nowClect.addChild(item)
            self._ui.homeui.infoList.setCurrentItem(item)
            new_job = JobInfo(name, 10, CPUTaskInfo(100, 1, 1000))
            sysSim.jobs[name] = new_job
            self.__initJobInfo(new_job)
        elif self.nowClect.text(0) == '故障':
            r = random.randint(0, 10000)
            name = "fault" + f"_{r}"
            while name in sysSim.faults:
                r = random.randint(0, 10000)
                name = "fault" + f"_{r}"
            item = QTreeWidgetItem([name])
            item.setFlags(item.flags())
            self.nowClect.addChild(item)
            self._ui.homeui.infoList.setCurrentItem(item)
            new_fault = FaultGenerator("Normal", 0, 0)
            if len(sysSim.hosts) > 0:
                new_fault.setAim(list(sysSim.hosts.keys())[0])
            new_fault.setName(name)
            sysSim.faults[name] = new_fault
            self._initFaultInfo(new_fault)


    def _applyHost(self):
        print("apply host")
        if self.nowHost is None:
            return
        name_before = self.nowHost.name
        self.nowHost.name = self.hostInfoPage.hostName.text()
        self.nowHost.ram = self.hostInfoPage.ram.value()
        cpunum = self.hostInfoPage.cpunum.value()
        cpucore = self.hostInfoPage.corenum.value()
        cpuflops = self.hostInfoPage.cpuflops.text()
        self.nowHost.cpu_infos = []
        for i in range(cpunum):
            self.nowHost.cpu_infos.append(CPUInfo(cpucore, cpuflops))
        self.nowHost.video_card_infos = []
        # 更新GPU
        if self.gpu_num > 0:
            self.nowHost.video_card_infos = []
            gpus = []
            for i in range(self.hostInfoPage.gputable.rowCount() - 1):
                gpu = GPUInfo(int(self.hostInfoPage.gputable.item(i + 1, 1).text()), (int)(self.hostInfoPage.gputable.item(i + 1, 2).text()), (int)(self.hostInfoPage.gputable.item(i+ 1, 3).text()), (int)(self.hostInfoPage.gputable.item(i+1, 5).text()), (int)(self.hostInfoPage.gputable.item(i+1, 4).text()))
                gpus.append(gpu)
                videoCardInfo = VideoCardInfo(gpus)
                videoCardInfo.pcie_bw = (int)(self.hostInfoPage.pcie.value()) 
            self.nowHost.video_card_infos.append(VideoCardInfo(gpus))
        self.nowHost.print()
        sysSim.hosts.pop(name_before)
        sysSim.hosts[self.nowHost.name] = self.nowHost
        self._initHostInfo(self.nowHost)
        # 更新树
        for i in range(self.nowClect.childCount()):
            if self.nowClect.child(i).text(0) == name_before:
                self.nowClect.child(i).setText(0, self.nowHost.name)
                break
        
    def _applyJob(self):
        print("apply job")
        if self.nowJob is None:
            return
        name_before = self.nowJob.name
        self.nowJob.name = self.jobInfoPage.jobName.text()
        self.nowJob.cpu_task.ram = self.jobInfoPage.ram.text()
        self.nowJob.period = self.jobInfoPage.period.text()
        self.nowJob.cpu_task.pes_number = self.jobInfoPage.corenum.value()
        self.nowJob.cpu_task.length = self.jobInfoPage.cpuflops.text()
        self.nowJob.gpu_task = None
        if self.kernel_num > 0:
            request_gddram_total = 0
            task_input_size_total = 0
            task_output_size_total = 0
            kernels = []
            for i in range(self.jobInfoPage.gputable.rowCount() - 1):
                request_gddram_total += int(self.jobInfoPage.gputable.item(i + 1, 4).text())
                task_input_size_total += int(self.jobInfoPage.gputable.item(i + 1, 5).text())
                task_output_size_total += int(self.jobInfoPage.gputable.item(i + 1, 6).text())
                kernel = GPUTaskInfo.Kernel(int(self.jobInfoPage.gputable.item(i + 1, 1).text()), int(self.jobInfoPage.gputable.item(i + 1, 2).text()), int(self.jobInfoPage.gputable.item(i + 1, 3).text()))
                kernels.append(kernel)
            self.nowJob.gpu_task = GPUTaskInfo(kernels, request_gddram_total, task_input_size_total, task_output_size_total)
        self.__initJobInfo(self.nowJob)
        sysSim.jobs.pop(name_before)
        sysSim.jobs[self.nowJob.name] = self.nowJob
        self.nowJob.print()
        # 更新树
        for i in range(self.nowClect.childCount()):
            if self.nowClect.child(i).text(0) == name_before:
                self.nowClect.child(i).setText(0, self.nowJob.name)
                break

    def _applyFault(self):
        print("apply fault")
        if self.nowFault is None:
            return
        name_before = self.nowFault.name
        newFault = FaultGenerator(tranFromC2E(self.faultInfoPage.type.currentText()), (float)(self.faultInfoPage.time1.text()), (float)(self.faultInfoPage.time2.text()))
        newFault.setAim(self.faultInfoPage.aim.currentText())
        newFault.setName(self.faultInfoPage.name.text())
        sysSim.faults.pop(name_before)
        sysSim.faults[newFault.name] = newFault
        self.nowFault = newFault
        newFault.print()
        self._initFaultInfo(newFault)
        # 更新树
        for i in range(self.nowClect.childCount()):
            if self.nowClect.child(i).text(0) == name_before:
                self.nowClect.child(i).setText(0, self.nowFault.name)
                break

    def _initHostInfo(self, host: HostInfo, ifTrueHost=True):
        self.gpu_num = 0
        self.cpushow.setChart(QChart())
        self.ramshow.setChart(QChart())
        self.gpushow.setChart(QChart())
        if ifTrueHost:
            self.nowHost = host
        else:
            self.nowHost = None
        if ifTrueHost:
            path = project.projectPath + "/OutputFiles/hostUtils.xml"
            if os.path.exists(path):
                xmlParser = XmlParser(path)
                self.cluster_result = xmlParser.parseHostRecord()
                painter = Painter(self.cluster_result, [], [])
                chartCPU = painter.plotHostCPUUtilization(host.name, -1, float("inf"))
                self.cpushow.setChart(chartCPU)
                chartRam = painter.plotHostRamUtilization(host.name, -1, float("inf"))
                self.ramshow.setChart(chartRam)
                chartGPU = painter.plotGpuUtilization(host.name, -1, -1, float("inf"))
                self.gpushow.setChart(chartGPU)
        self.hostInfoPage.hostName.setText(host.name)
        self.hostInfoPage.ram.setValue(host.ram)
        cpunum = len(host.cpu_infos)
        cpucore = host.cpu_infos[0].cores
        self.hostInfoPage.corenum.setValue(cpucore)
        self.hostInfoPage.cpunum.setValue(cpunum)
        self.hostInfoPage.cpuflops.setText(str(host.cpu_infos[0].mips))
        reg_ex =  QRegularExpression("[0-9]+")
        validator = QRegularExpressionValidator(reg_ex, self.hostInfoPage.cpuflops)
        self.hostInfoPage.cpuflops.setValidator(validator)
        self._ui.homeui.tabWidget.setCurrentIndex(0)
        if host.video_card_infos != []:
            gpu_num = len(host.video_card_infos[0].gpu_infos)
            if gpu_num > 0:
                self.gpu_num = gpu_num
                self.initGpuTable(gpu_num, host.video_card_infos[0].gpu_infos)
            else:
                self.gpu_num = 0
                self.initGpuTable(0, [])
        else:
            self.gpu_num = 0
            self.initGpuTable(0, [])
                
    def initGpuTable(self, gpu_num, gpu_infos):    
        delegate = NumericDelegate(self.hostInfoPage.gputable)
        self.hostInfoPage.gputable.setItemDelegate(delegate)
        self.hostInfoPage.gputable.setColumnCount(7)
        self.hostInfoPage.gputable.setRowCount(gpu_num + 1)
        # 设置不可见
        self.hostInfoPage.gputable.verticalHeader().setVisible(False)
        self.hostInfoPage.gputable.horizontalHeader().setVisible(False)
        i = 0
        # self.hostInfoPage.gputable.setItem(i, 0, QTableWidgetItem("GPU ID"))
        # self.hostInfoPage.gputable.setItem(i, 1, QTableWidgetItem("GPU 核心数"))
        # self.hostInfoPage.gputable.setItem(i, 2, QTableWidgetItem("GPU 每流处理器核心数"))
        # self.hostInfoPage.gputable.setItem(i, 3, QTableWidgetItem("GPU 每流处理器最大线程块数"))
        # self.hostInfoPage.gputable.setItem(i, 4, QTableWidgetItem("GPU 核心FLOPs"))
        # self.hostInfoPage.gputable.setItem(i, 5, QTableWidgetItem("GPU 显存"))
        # 第一行背景设为灰色，信息如上所示
        item1 = QTableWidgetItem("GPU ID")
        item1.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 0, item1)
        item2 = QTableWidgetItem("核心数")
        item2.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 1, item2)
        item3 = QTableWidgetItem("SM核心数")
        item3.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 2, item3)
        item4 = QTableWidgetItem("SM最大线程块数")
        item4.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 3, item4)
        item5 = QTableWidgetItem("核心FLOPs")
        item5.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 4, item5)
        item6 = QTableWidgetItem("显存(GB)")
        item6.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 5, item6)

        for gpu_info in gpu_infos:
            i += 1
            self.hostInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
            self.hostInfoPage.gputable.setItem(i, 1, QTableWidgetItem(str(gpu_info.cores)))
            self.hostInfoPage.gputable.setItem(i, 2, QTableWidgetItem(str(gpu_info.core_per_sm)))
            self.hostInfoPage.gputable.setItem(i, 3, QTableWidgetItem(str(gpu_info.max_block_per_sm))
            )
            self.hostInfoPage.gputable.setItem(i, 4, QTableWidgetItem(str(gpu_info.flops_per_core)))
            self.hostInfoPage.gputable.setItem(i, 5, QTableWidgetItem(str(gpu_info.gddram)))
            del_gpu = QPushButton()
            del_gpu.setText("删除")
            del_gpu.clicked.connect(self._delGpu)
            self.hostInfoPage.gputable.setCellWidget(i, 6, del_gpu)

    def _delGpu(self):
        print("del gpu")
        row = self.hostInfoPage.gputable.currentRow()
        self.hostInfoPage.gputable.removeRow(row)
        self.gpu_num -= 1
        for i in range(row, self.gpu_num + 1):
            self.hostInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))

    def _addGpu(self):
        if self.nowHost is None:
            return
        self.gpu_num += 1
        self.hostInfoPage.gputable.setRowCount(self.gpu_num + 1)
        i = self.gpu_num
        if self.gpu_num == 1:
            self.hostInfoPage.gputable.setColumnCount(7)
            item1 = QTableWidgetItem("GPU ID")
            item1.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 0, item1)
            item2 = QTableWidgetItem("核心数")
            item2.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 1, item2)
            item3 = QTableWidgetItem("SM核心数")
            item3.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 2, item3)
            item4 = QTableWidgetItem("SM最大线程块数")
            item4.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 3, item4)
            item5 = QTableWidgetItem("核心FLOPs")
            item5.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 4, item5)
            item6 = QTableWidgetItem("显存(GB)")
            item6.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 5, item6)

        self.hostInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
        self.hostInfoPage.gputable.setItem(i, 1, QTableWidgetItem("0"))
        self.hostInfoPage.gputable.setItem(i, 2, QTableWidgetItem("0"))
        self.hostInfoPage.gputable.setItem(i, 3, QTableWidgetItem("0"))
        self.hostInfoPage.gputable.setItem(i, 4, QTableWidgetItem("0"))
        self.hostInfoPage.gputable.setItem(i, 5, QTableWidgetItem("0"))
        del_gpu = QPushButton()
        del_gpu.setText("删除")
        del_gpu.clicked.connect(self._delGpu)
        self.hostInfoPage.gputable.setCellWidget(i, 6, del_gpu)

    def __initJobInfo(self, job: JobInfo, ifTrueJob=True):
        if ifTrueJob:
            self.nowJob = job
        else:
            self.nowJob = None
        if ifTrueJob:
            path = project.projectPath + "/OutputFiles/jobRun.xml"
            if os.path.exists(path):
                xmlParser = XmlParser(path)
                self.job_result = xmlParser.parseJobRecord()
                painter = Painter([], self.job_result, [])
                chart = painter.plotJobDuration(job.name)
                self.jobInfoPage.showjob.setChart(chart)
        self.jobInfoPage.jobName.setText(job.name)
        self.jobInfoPage.ram.setText(str(job.cpu_task.ram))
        reg_ex =  QRegularExpression("[0-9]+")
        validator = QRegularExpressionValidator(reg_ex, self.jobInfoPage.ram)
        self.jobInfoPage.ram.setValidator(validator)
        self.jobInfoPage.period.setText(str(job.period))
        reg_ex =  QRegularExpression("[0-9]+")
        validator = QRegularExpressionValidator(reg_ex, self.jobInfoPage.period)
        self.jobInfoPage.period.setValidator(validator)
        self.jobInfoPage.corenum.setValue(job.cpu_task.pes_number)
        self.jobInfoPage.cpuflops.setText(str(job.cpu_task.length))
        reg_ex =  QRegularExpression("[0-9]+")
        validator = QRegularExpressionValidator(reg_ex, self.jobInfoPage.cpuflops)
        self.jobInfoPage.cpuflops.setValidator(validator)
        if job.gpu_task is not None:
            print("gpu task")
            self.kernel_num = len(job.gpu_task.kernels)
            self._initKernelTable(len(job.gpu_task.kernels), job.gpu_task)
        else:
            print("no gpu task")
            self.kernel_num = 0
            self._initKernelTable(0, None)
        self._ui.homeui.tabWidget.setCurrentIndex(1)

    def _initKernelTable(self, kernel_num, gpu_task):
        delegate = NumericDelegate(self.jobInfoPage.gputable)
        self.jobInfoPage.gputable.setItemDelegate(delegate)
        self.jobInfoPage.gputable.setColumnCount(8)
        self.jobInfoPage.gputable.setRowCount(kernel_num + 1)
        # 设置不可见
        self.jobInfoPage.gputable.verticalHeader().setVisible(False)
        self.jobInfoPage.gputable.horizontalHeader().setVisible(False)
        i = 0
        item1 = QTableWidgetItem("内核 ID")
        item1.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 0, item1)
        item2 = QTableWidgetItem("线程块数")
        item2.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 1, item2)
        item3 = QTableWidgetItem("线程数")
        item3.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 2, item3)
        item4 = QTableWidgetItem("每线程FLOP")
        item4.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 3, item4)
        item5 = QTableWidgetItem("需求显存(MB)")    
        item5.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 4, item5)
        item6 = QTableWidgetItem("输入(MB)")
        item6.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 5, item6)
        item7 = QTableWidgetItem("输出(MB)")
        item7.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 6, item7)
        i = 0
        if gpu_task is not None:
            for kernel_info in gpu_task.kernels:
                i += 1
                self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
                self.jobInfoPage.gputable.setItem(i, 1, QTableWidgetItem(str(kernel_info.block_num)))
                self.jobInfoPage.gputable.setItem(i, 2, QTableWidgetItem(str(kernel_info.thread_num)))
                self.jobInfoPage.gputable.setItem(i, 3, QTableWidgetItem(str(kernel_info.thread_length)))
                self.jobInfoPage.gputable.setItem(i, 4, QTableWidgetItem(str(gpu_task.requested_gddram_size)))
                self.jobInfoPage.gputable.setItem(i, 5, QTableWidgetItem(str(gpu_task.task_input_size)))
                self.jobInfoPage.gputable.setItem(i, 6, QTableWidgetItem(str(gpu_task.task_output_size)))
                del_kernel = QPushButton()
                del_kernel.setText("删除")
                del_kernel.clicked.connect(self._delKernel)
                self.jobInfoPage.gputable.setCellWidget(i, 7, del_kernel)
        

    def _delKernel(self):
        print("del kernel")
        row = self.jobInfoPage.gputable.currentRow()
        self.jobInfoPage.gputable.removeRow(row)
        self.kernel_num -= 1
        for i in range(row, self.kernel_num + 1):
            self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))

    def _addKernel(self):
        if self.nowJob is None:
            return
        self.kernel_num += 1
        print("add kernel: " + str(self.kernel_num))
        self.jobInfoPage.gputable.setRowCount(self.kernel_num + 1)
        i = self.kernel_num
        if self.kernel_num == 1:
            self.jobInfoPage.gputable.setColumnCount(8)
            item1 = QTableWidgetItem("内核 ID")
            item1.setBackground(QColor(192, 192, 192))
            self.jobInfoPage.gputable.setItem(0, 0, item1)
            item2 = QTableWidgetItem("线程块数")
            item2.setBackground(QColor(192, 192, 192))
            self.jobInfoPage.gputable.setItem(0, 1, item2)
            item3 = QTableWidgetItem("线程数")
            item3.setBackground(QColor(192, 192, 192))
            self.jobInfoPage.gputable.setItem(0, 2, item3)
            item4 = QTableWidgetItem("每线程FLOP")
            item4.setBackground(QColor(192, 192, 192))
            self.jobInfoPage.gputable.setItem(0, 3, item4)
            item5 = QTableWidgetItem("需求显存(MB)")    
            item5.setBackground(QColor(192, 192, 192))
            self.jobInfoPage.gputable.setItem(0, 4, item5)
            item6 = QTableWidgetItem("输入(MB)")
            item6.setBackground(QColor(192, 192, 192))
            self.jobInfoPage.gputable.setItem(0, 5, item6)
            item7 = QTableWidgetItem("输出(MB)")
            item7.setBackground(QColor(192, 192, 192))
            self.jobInfoPage.gputable.setItem(0, 6, item7)
            del_kernel = QPushButton()
            del_kernel.setText("删除")
            del_kernel.clicked.connect(self._delKernel)
            self.jobInfoPage.gputable.setCellWidget(0, 7, del_kernel)

        self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
        self.jobInfoPage.gputable.setItem(i, 1, QTableWidgetItem("0"))
        self.jobInfoPage.gputable.setItem(i, 2, QTableWidgetItem("0"))
        self.jobInfoPage.gputable.setItem(i, 3, QTableWidgetItem("0"))
        self.jobInfoPage.gputable.setItem(i, 4, QTableWidgetItem("0"))
        self.jobInfoPage.gputable.setItem(i, 5, QTableWidgetItem("0"))
        self.jobInfoPage.gputable.setItem(i, 6, QTableWidgetItem("0"))


    def _initFaultInfo(self, fault: FaultGenerator, ifTrueFault=True):
        if ifTrueFault:
            print(fault.mttf_type + " 是这个")
            self.nowFault = fault
            self.faultInfoPage.aim.clear()
            self.faultInfoPage.aim.addItems(sysSim.hosts.keys())
            self.faultInfoPage.name.setText(fault.name)
            self.faultInfoPage.aim.setCurrentText(fault.aim)
            self.faultInfoPage.type.setCurrentText(tranFromE2C(fault.mttf_type))
            print(tranFromE2C(fault.mttf_type))
            self.faultInfoPage.time1.setText(str(fault.mttf_scale))
            regular_ex = QRegularExpression("[0-9]+")
            validator = QRegularExpressionValidator(regular_ex, self.faultInfoPage.time1)
            self.faultInfoPage.time1.setValidator(validator)
            self.faultInfoPage.time2.setText(str(fault.mttr_scale))
            regular_ex = QRegularExpression("[0-9]+")
            validator = QRegularExpressionValidator(regular_ex, self.faultInfoPage.time2)
            self.faultInfoPage.time2.setValidator(validator)
            self._ui.homeui.tabWidget.setCurrentIndex(2)
            if fault.mttf_type == "Normal":
                self.faultInfoPage.show.setChart(self.__getNormalLine(fault.mttf_scale))
                self.faultInfoPage.show2.setChart(self.__getNormalLine(fault.mttr_scale))
            elif fault.mttf_type == "LogNormal":
                self.faultInfoPage.show.setChart(self.__getLogNormalLine(fault.mttf_scale))
                self.faultInfoPage.show2.setChart(self.__getLogNormalLine(fault.mttr_scale))
            elif fault.mttf_type == "Weibull":
                self.faultInfoPage.show.setChart(self.__getWeiBullLine(fault.mttf_scale))
                self.faultInfoPage.show2.setChart(self.__getWeiBullLine(fault.mttr_scale))
            elif fault.mttf_type == "Gamma":
                self.faultInfoPage.show.setChart(self.__getGammaLine(fault.mttf_scale))
                self.faultInfoPage.show2.setChart(self.__getGammaLine(fault.mttr_scale))
        else:
            self.nowFault = None
            self.faultInfoPage.aim.clear()
            #self.faultInfoPage.aim.addItems(sysSim.hosts.keys())
            self.faultInfoPage.name.setText("")
            self.faultInfoPage.aim.setCurrentText("")
            self.faultInfoPage.type.setCurrentText("")
            self.faultInfoPage.time1.setText("")
            regular_ex = QRegularExpression("[0-9]+")
            validator = QRegularExpressionValidator(regular_ex, self.faultInfoPage.time1)
            self.faultInfoPage.time1.setValidator(validator)
            self.faultInfoPage.time2.setText("")
            regular_ex = QRegularExpression("[0-9]+")
            validator = QRegularExpressionValidator(regular_ex, self.faultInfoPage.time2)
            self.faultInfoPage.time2.setValidator(validator)
            self._ui.homeui.tabWidget.setCurrentIndex(2)
            self.faultInfoPage.show.setChart(QChart())

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
        print("delete")
        if self.nowClect is None:
            print("none")
            return
        if self.nowClect.text(0) == '主机':
            sysSim.hosts.pop(self._ui.homeui.infoList.currentItem().text(0))
            self._ui.homeui.tabWidget.setCurrentIndex(0)
            self._initHostInfo(HostInfo("", [], [CPUInfo(0, 0)], 0), False)
        elif self.nowClect.text(0) == '任务':
            sysSim.jobs.pop(self._ui.homeui.infoList.currentItem().text(0))
            self._ui.homeui.tabWidget.setCurrentIndex(1)
            self.__initJobInfo(JobInfo("", 0, CPUTaskInfo(0, 0, 0)), False)
        elif self.nowClect.text(0) == '故障':
            sysSim.faults.pop(self._ui.homeui.infoList.currentItem().text(0))
            self._ui.homeui.tabWidget.setCurrentIndex(2)
            fault = FaultGenerator("正态分布", 0, 0)
            fault.setAim("")
            fault.setName("")
            self._initFaultInfo(FaultGenerator("正态分布", 0, 0), False)
        self.nowClect.removeChild(self._ui.homeui.infoList.currentItem())
    
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
        execute = "java -jar ./jobSim/gpuworkflowsim.jar " + project.projectPath + "/OutputFiles " + project.projectPath + "/hosts.json " + project.projectPath + "/jobs.json " + project.projectPath + "/faults.json " + str(0) + " " + str(self.duration)
        print(execute)
        popen = subprocess.Popen(execute, shell=True, stdout=subprocess.PIPE,  universal_newlines=True, stderr=subprocess.STDOUT)
        out,err = popen.communicate()
        # print('std_out: ' + out)
        #将日志信息显示在文本框中
        self._ui.homeui.textEdit.setText(out)
        if "任务群总完成时间" in out:
            QMessageBox.information(self, "", "仿真完成")
        self._ui.central_window.centralWidget().setEnabled(True)
        self._initResult()
        self._ui.stack_widget.setCurrentIndex(1)

    def _initResult(self):
        # 去除之前的记录
        self._ui.resultui.hostTabs.clear()
        self._ui.resultui.jobTabs.clear()
        self._ui.resultui.faultTabs.clear()
        self._ui.resultui.show.setChart(QChart())
        self._ui.resultui.showCPU.setChart(QChart())
        self._ui.resultui.showRam.setChart(QChart())
        self._ui.resultui.showGPU.setChart(QChart())
        self._ui.resultui.faultResultAnalysis.setChart(QChart())
        self._ui.resultui.jobResultAnalysis.setChart(QChart())

        # 绘制折线图
        path = project.projectPath + "/OutputFiles/hostUtils.xml"
        xmlParser = XmlParser(path)
        self.cluster_result = xmlParser.parseHostRecord()
        path = project.projectPath + "/OutputFiles/jobRun.xml"
        xmlParser = XmlParser(path)
        self.job_results = xmlParser.parseJobRecord()
        path = project.projectPath + "/OutputFiles/faultRecords.xml"
        xmlParser = XmlParser(path)
        self.fault_results = xmlParser.parseFaultRecord()


        self.reliable = xmlParser.parseReliabilityRecord()
        # 保留两位小数
        self.reliable = round(self.reliable, 2)
        self.pieSeries = QPieSeries()
        self.pieSeries.append("余度可靠性:" + str(self.reliable * 100) + "%", self.reliable * 100)
        self.pieSeries.append(":" + str((1 - self.reliable) * 100) + "%", (1 - self.reliable) * 100)
        self.pieSeries.setPieSize(0.5)
        # self.pieSeries.setPieStartAngle(startAngle)
        # self.pieSeries.setPieEndAngle(endAngle)
        percent_total = 0
        for job in self.job_results:
            name = job.jobName
            duration = sysSim.jobs[name].period
            percent = 0
            for jobRun in job.jobRuns:
                percent += (float)(jobRun.duration) / (float)(duration)
            percent /= len(job.jobRuns)
            percent_total += percent
        percent_total /= len(self.job_results)
        percent_total = 1 - percent_total
        # 保留两位小数
        percent_total = round(percent_total, 2)
        self.jobSeries = QPieSeries()
        self.jobSeries.append("任务平均利用率\n" + str(percent_total * 100) + "%", percent_total * 100)
        self.jobSeries.append(":" + str((1 - percent_total) * 100) + "%", (1 - percent_total) * 100)
        self.jobSeries.setPieSize(0.5)
    

        chart = QChart()
        chart.addSeries(self.pieSeries)
        chart.setTitle("余度可靠性\n" + str(self.reliable * 100) + "%")
        chart.legend().hide()
        self._ui.resultui.faultResultAnalysis.setChart(chart)
        # 抗锯齿
        self._ui.resultui.faultResultAnalysis.setRenderHint(QPainter.Antialiasing)
        self._ui.resultui.faultResultAnalysis.setRenderHint(QPainter.TextAntialiasing)

        chart = QChart()
        chart.addSeries(self.jobSeries)
        chart.setTitle("计算效率\n" + str(percent_total * 100) + "%")
        chart.legend().hide()
        self._ui.resultui.jobResultAnalysis.setChart(chart)
        # 抗锯齿
        self._ui.resultui.jobResultAnalysis.setRenderHint(QPainter.Antialiasing)
        self._ui.resultui.jobResultAnalysis.setRenderHint(QPainter.TextAntialiasing)

        self.avergaeRunTime = 0.0
        for job in self.job_results:
            self.avergaeRunTime += getAverageRunTime(job)
        self.avergaeRunTime /= len(self.job_results)
        self.avergaeRunTime = round(self.avergaeRunTime, 2)
        self.pieSeries = QPieSeries()
        self.pieSeries.append("平均运行\n" + str(self.avergaeRunTime) + "s", self.avergaeRunTime)
        self.pieSeries.append(":" + str(self.duration - self.avergaeRunTime) + "s", self.duration - self.avergaeRunTime)
        self.pieSeries.setPieSize(0.5)

        chart = QChart()
        chart.addSeries(self.pieSeries)
        chart.setTitle("平均运行\n" + str(self.avergaeRunTime) + "s")
        chart.legend().hide()
        self._ui.resultui.jobResultAnalysis2.setChart(chart)
        # 抗锯齿
        self._ui.resultui.jobResultAnalysis2.setRenderHint(QPainter.Antialiasing)
        self._ui.resultui.jobResultAnalysis2.setRenderHint(QPainter.TextAntialiasing)

        self.throughput = (int)(getThroughput(self.job_results))
        self.pieSeries = QPieSeries()
        self.pieSeries.append(str(self.throughput) + "FLOPS/s", self.throughput)
        # self.pieSeries.append(":" + str(100 - self.throughput) + "FLOPS/s", 100 - self.throughput)
        self.pieSeries.setPieSize(0.5)

        chart = QChart()
        chart.addSeries(self.pieSeries)
        chart.setTitle("吞吐\n" + str(self.throughput) + "/s")
        chart.legend().hide()
        self._ui.resultui.jobResultAnalysis3.setChart(chart)
        # 抗锯齿
        self._ui.resultui.jobResultAnalysis3.setRenderHint(QPainter.Antialiasing)
        self._ui.resultui.jobResultAnalysis3.setRenderHint(QPainter.TextAntialiasing)




        self.painter = Painter(self.cluster_result, self.job_results, self.fault_results)

        # 填充主机信息表格
        host_num = len(self.cluster_result.hostRecords)
        self.hostTable = QTableWidget()
        # 设置不可见
        self.hostTable.verticalHeader().setVisible(False)
        self.hostTable.horizontalHeader().setVisible(True)
        self.hostTable.setColumnCount(5)
        self.hostTable.setRowCount(host_num)
        self.hostTable.setHorizontalHeaderLabels(["主机名", "CPU(平均/最大)", "内存(平均/最大)", "GPU(平均/最大)",""])
        i = 0
        for hostRecord in self.cluster_result.hostRecords:
            hostRecord.calculateUtilization()
            cpu = f"{hostRecord.avgCpuUtilization:.2f}/{hostRecord.maxCpuUtilization:.2f}"
            ram = f"{hostRecord.avgRamUtilization:.2f}/{hostRecord.maxRamUtilization:.2f}"
            gpu = f"{hostRecord.avgGpuUtilization:.2f}/{hostRecord.maxGpuUtilization:.2f}"
            seeMore = QPushButton()
            seeMore.setText("查看")
            seeMore.clicked.connect(partial(self._initChartView, hostRecord.hostName))
            self.hostTable.setItem(i, 0, QTableWidgetItem(hostRecord.hostName))
            self.hostTable.setItem(i, 1, QTableWidgetItem(cpu))
            self.hostTable.setItem(i, 2, QTableWidgetItem(ram))
            self.hostTable.setItem(i, 3, QTableWidgetItem(gpu))
            self.hostTable.setCellWidget(i, 4, seeMore)
            i += 1
        self._ui.resultui.hostTabs.addTab(self.hostTable, "主机利用率")

        # 填充任务信息表格
        job_num = len(self.job_results)
        self.jobTable = QTableWidget()
        # 设置不可见
        self.jobTable.verticalHeader().setVisible(False)
        self.jobTable.horizontalHeader().setVisible(True)
        self.jobTable.setColumnCount(5)
        self.jobTable.setRowCount(job_num)
        self.jobTable.setHorizontalHeaderLabels(["任务名", "运行次数", "成功次数", "超时次数",""])
        i = 0
        for jobRecord in self.job_results:
            seeMore = QPushButton()
            seeMore.setText("查看")
            seeMore.clicked.connect(partial(self._initJobChartView, jobRecord))
            total = 0
            suc = 0
            timeout = 0
            for jobRun in jobRecord.jobRuns:
                total += 1
                if jobRun.status == "Success":
                    suc += 1
                else:
                    timeout += 1
            self.jobTable.setItem(i, 0, QTableWidgetItem(jobRecord.jobName))
            self.jobTable.setItem(i, 1, QTableWidgetItem(str(total)))
            self.jobTable.setItem(i, 2, QTableWidgetItem(str(suc)))
            self.jobTable.setItem(i, 3, QTableWidgetItem(str(timeout)))
            self.jobTable.setCellWidget(i, 4, seeMore)
            i += 1
        self._ui.resultui.jobTabs.addTab(self.jobTable, "任务运行情况")
        self.jobRunTable = QTableWidget()
        # 设置不可见
        self.jobRunTable.verticalHeader().setVisible(False)
        self.jobRunTable.horizontalHeader().setVisible(True)
        self.jobRunTable.setColumnCount(5)
        self.jobRunTable.setRowCount(0)
        self.jobRunTable.setHorizontalHeaderLabels(["任务名", "主机", "开始", "结束","状态"])
        self._ui.resultui.jobTabs.addTab(self.jobRunTable, "任务运行记录")
        self.jobChart = QChartView()
        self._ui.resultui.jobTabs.addTab(self.jobChart, "任务运行图表")

        # 填充故障信息表格
        fault_num = len(self.fault_results)
        self.faultTable = QTableWidget()
        # 设置不可见
        self.faultTable.verticalHeader().setVisible(False)
        self.faultTable.horizontalHeader().setVisible(True)
        self.faultTable.setColumnCount(4)
        self.faultTable.setRowCount(fault_num)
        self.faultTable.setHorizontalHeaderLabels(["时间", "故障对象", "类型", ""])
        i = 0
        for faultRecord in self.fault_results:
            seeMore = QPushButton()
            seeMore.setText("查看")
            seeMore.clicked.connect(partial(self._initFaultResult, faultRecord))
            self.faultTable.setItem(i, 0, QTableWidgetItem(faultRecord.time))
            self.faultTable.setItem(i, 1, QTableWidgetItem(faultRecord.object))
            self.faultTable.setItem(i, 2, QTableWidgetItem(faultRecord.type))
            self.faultTable.setCellWidget(i, 3, seeMore)
            i += 1
        self._ui.resultui.faultTabs.addTab(self.faultTable, "故障记录")
        self.faultMoreTable = QTableWidget()
        # 设置不可见
        self.faultMoreTable.verticalHeader().setVisible(False)
        self.faultMoreTable.horizontalHeader().setVisible(True)
        self.faultMoreTable.setColumnCount(4)
        self.faultMoreTable.setRowCount(0)
        self.faultMoreTable.setHorizontalHeaderLabels(["是否虚警", "重构成功", "可靠度(前)", "可靠度(后)"])
        self._ui.resultui.faultTabs.addTab(self.faultMoreTable, "故障详细信息")

    def _initChartView(self, hostName):
        chart = self.painter.plotHostUtilization(hostName, -1, float("inf"))
        self._ui.resultui.show.setChart(chart)
        chartCPU = self.painter.plotHostCPUUtilization(hostName, -1, float("inf"))
        self._ui.resultui.showCPU.setChart(chartCPU)
        chartRam = self.painter.plotHostRamUtilization(hostName, -1, float("inf"))
        self._ui.resultui.showRam.setChart(chartRam)
        chartGPU = self.painter.plotGpuUtilization(hostName, -1, -1, float("inf"))
        self._ui.resultui.showGPU.setChart(chartGPU)

    def _initJobChartView(self, jobRecord):
        # 清除jobRunTable表格
        self.jobRunTable.setRowCount(0)
        run_num = len(jobRecord.jobRuns)
        self.jobRunTable.setRowCount(run_num)
        i = 0
        for jobRun in jobRecord.jobRuns:
            self.jobRunTable.setItem(i, 0, QTableWidgetItem(jobRecord.jobName))
            self.jobRunTable.setItem(i, 1, QTableWidgetItem(jobRun.host))
            self.jobRunTable.setItem(i, 2, QTableWidgetItem(jobRun.start))
            self.jobRunTable.setItem(i, 3, QTableWidgetItem(jobRun.end))
            if jobRun.status == 'Success':
                self.jobRunTable.setItem(i, 4, QTableWidgetItem("成功"))
            else:
                self.jobRunTable.setItem(i, 4, QTableWidgetItem("超时"))
            i += 1

        chart = self.painter.plotJobDuration(jobRecord.jobName)
        self._ui.resultui.jobTabs.setCurrentIndex(1)
        self.jobChart.setChart(chart)

    def _initFaultResult(self, faultRecord):
        self.faultMoreTable.setRowCount(1)
        print(faultRecord.isFalseAlarm)
        if faultRecord.isFalseAlarm == "True":
            self.faultMoreTable.setItem(0, 0, QTableWidgetItem("是"))
        else:
            self.faultMoreTable.setItem(0, 0, QTableWidgetItem("否"))
        if faultRecord.type == "任务超时":
            self.faultMoreTable.setItem(0, 1, QTableWidgetItem("\\"))
            self.faultMoreTable.setItem(0, 2, QTableWidgetItem("\\"))
            self.faultMoreTable.setItem(0, 3, QTableWidgetItem("\\"))
            self._ui.resultui.faultTabs.setCurrentIndex(1)
            return
        else:
            if faultRecord.isSuccessRebuild == "True":
                self.faultMoreTable.setItem(0, 1, QTableWidgetItem("是"))
            else:
                self.faultMoreTable.setItem(0, 1, QTableWidgetItem("否"))
        
        self.faultMoreTable.setItem(0, 2, QTableWidgetItem(str(faultRecord.redundancyBefore)))
        self.faultMoreTable.setItem(0, 3, QTableWidgetItem(str(faultRecord.redundancyAfter)))
        self._ui.resultui.faultTabs.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(sys.argv)
    # if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):  # Enable High DPI display with Qt5
    #     app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    # QDir.addSearchPath("icons", f"{get_project_root_path().as_posix()}/widget_gallery/ui/svg")
    win = JobSimQt(sys.argv[1])
    win.menuBar().setNativeMenuBar(False)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    win.show()
    app.exec()
