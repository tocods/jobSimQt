# ---------------------------------------------------------------------------------------------
#  Copyright (c) Yunosuke Ohsugi. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------*/

import sys
import numpy as np
from scipy import stats
import random
from functools import partial
import qdarktheme
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot
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

class JobSimQt(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # 取消标题栏
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.nowClect = None
        self._ui = UI()
        self._ui.setup_ui(self)

        # Signal
        self._ui.action_change_home.triggered.connect(self._change_page)
        self._ui.action_change_dock.triggered.connect(self._change_page)
        self._ui.action_open_folder.triggered.connect(
            lambda: QFileDialog.getOpenFileName(self, "Open File", options=QFileDialog.Option.DontUseNativeDialog)
        )
        self._ui.action_open_color_dialog.triggered.connect(
            lambda: QColorDialog.getColor(parent=self, options=QColorDialog.ColorDialogOption.DontUseNativeDialog)
        )
        self._ui.action_open_font_dialog.triggered.connect(
            lambda: QFontDialog.getFont(QFont(), parent=self, options=QFontDialog.FontDialogOption.DontUseNativeDialog)
        )
        self._ui.action_enable.triggered.connect(self._toggle_state)
        self._ui.action_disable.triggered.connect(self._toggle_state)
        for action in self._ui.actions_theme:
            action.triggered.connect(self._change_theme)

        self._initAll()
        self.initTreeView()
        self.setClicked()

    @Slot()
    def _change_page(self) -> None:
        action_name = self.sender().text()
        self._ui.stack_widget.setCurrentIndex(0 if action_name == "Move to home" else 1)

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
        QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet(theme))

    def setClicked(self):
        self._ui.homeui.add.clicked.connect(self._add)
        self._ui.homeui.pushButton.clicked.connect(self._delete)
        self._ui.homeui.textEdit.setReadOnly(True)
        self._ui.homeui.run.clicked.connect(self._run)

    def _initAll(self):
        self.nowHost = None
        self.nowJob = None
        self.nowFault = None
        path = "project/hosts.json"
        parser = ParseUtil()
        self.hosts = parser.parseHosts(path)
        print(self.hosts)
        for host in self.hosts:
            sysSim.hosts[host.name] = host
        path = "project/jobs.json"
        self.jobs = parser.parseJobs(path)
        for job in self.jobs:
            sysSim.jobs[job.name] = job
        path = "project/faults.json"
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
        screesize = self._ui.homeui.tabWidget.size()
        w.setGeometry(0, 0, screesize.width(), screesize.height())

        j = QWidget()
        self.jobInfoPage = Ui_JobInfo()
        self.jobInfoPage.setupUi(j)
        self.jobInfoPage.pushButton.setIcon(QIcon("img/加.png"))
        self.jobInfoPage.apply.clicked.connect(self._applyJob)
        self._ui.homeui.tabWidget.addTab(j, "任务")
        j.setGeometry(0, 0, screesize.width(), screesize.height())

        f = QWidget()
        self.faultInfoPage = Ui_FaultInfo()
        self.faultInfoPage.setupUi(f)
        self.faultInfoPage.apply.clicked.connect(self._applyFault)
        self._ui.homeui.tabWidget.addTab(f, "故障")
        f.setGeometry(0, 0, screesize.width(), screesize.height())

        self._initResult()


    def initTreeView(self):
        screen = QGuiApplication.screens()[0]
        screen_size = screen.availableGeometry()
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
        self._ui.homeui.infoList.clicked.connect(self._showInfo)
        self._ui.homeui.infoList.setHeaderHidden(True)
        self.setGeometry(0, 0, screen_size.width() * 0.9, screen_size.height() * 0.9)
        self._ui.homeui.widget.setGeometry(0, 0, screen_size.width() * 0.7, screen_size.height() * 0.7)
        self._ui.resultui.layoutWidget.setGeometry(0, 0, screen_size.width() * 0.9, screen_size.height() * 0.7)


    def _showInfo(self):
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
        r = random.randint(0, 10000)
        name = self.nowClect.text(0) + f"_{r}"
        item = QTreeWidgetItem([name])
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.nowClect.addChild(item)
        if self.nowClect.text(0) == '主机':
            while name in sysSim.hosts:
                r = random.randint(0, 10000)
                name = self.nowClect.text(0) + f"_{r}"
            new_host = HostInfo(name, [], [CPUInfo(2, 1000)], 4)
            sysSim.hosts[name] = new_host
            self._initHostInfo(new_host)
        elif self.nowClect.text(0) == '任务':
            while name in sysSim.jobs:
                r = random.randint(0, 10000)
                name = self.nowClect.text(0) + f"_{r}"
            new_job = JobInfo(name, 10, CPUTaskInfo(100, 1, 1000))
            sysSim.jobs[name] = new_job
            self.__initJobInfo(new_job)
        elif self.nowClect.text(0) == '故障':
            while name in sysSim.faults:
                r = random.randint(0, 10000)
                name = self.nowClect.text(0) + f"_{r}"
            new_fault = FaultGenerator("正态分布", 0, 0)
            new_fault.setAim(sysSim.hosts.keys()[0])
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
        for i in range(cpunum):
            self.nowHost.cpu_infos.append(CPUInfo(cpucore, cpuflops))
        # 更新GPU
        if self.gpu_num > 0:
            self.nowHost.video_card_infos = []
            gpus = []
            for i in range(self.hostInfoPage.gputable.rowCount() - 1):
                gpu = GPUInfo(int(self.hostInfoPage.gputable.item(i + 1, 1).text()), (int)(self.hostInfoPage.gputable.item(i + 1, 2).text()), (int)(self.hostInfoPage.gputable.item(i+ 1, 3).text()), (int)(self.hostInfoPage.gputable.item(i+1, 5).text()), (int)(self.hostInfoPage.gputable.item(i+1, 4).text()))
                gpus.append(gpu)
            self.nowHost.video_card_infos.append(VideoCardInfo(gpus))
        self.nowHost.print()
        sysSim.hosts.pop(name_before)
        sysSim.hosts[self.nowHost.name] = self.nowHost
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
        if ifTrueHost:
            self.nowHost = host
        else:
            self.nowHost = None
        self.hostInfoPage.hostName.setText(host.name)
        self.hostInfoPage.ram.setValue(host.ram)
        cpunum = len(host.cpu_infos)
        cpucore = cpunum * host.cpu_infos[0].cores
        self.hostInfoPage.corenum.setValue(cpucore)
        self.hostInfoPage.cpunum.setValue(cpunum)
        self.hostInfoPage.cpuflops.setText(str(host.cpu_infos[0].mips))
        self._ui.homeui.tabWidget.setCurrentIndex(0)
        if host.video_card_infos != []:
            gpu_num = len(host.video_card_infos[0].gpu_infos)
            if gpu_num > 0:
                self.gpu_num = gpu_num
                self.initGpuTable(gpu_num, host.video_card_infos[0].gpu_infos)
                
    def initGpuTable(self, gpu_num, gpu_infos):    
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
        item2 = QTableWidgetItem("GPU 核心数")
        item2.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 1, item2)
        item3 = QTableWidgetItem("GPU 每流处理器核心数")
        item3.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 2, item3)
        item4 = QTableWidgetItem("GPU 每流处理器最大线程块数")
        item4.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 3, item4)
        item5 = QTableWidgetItem("GPU 核心FLOPs")
        item5.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 4, item5)
        item6 = QTableWidgetItem("GPU 显存")
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
            item2 = QTableWidgetItem("GPU 核心数")
            item2.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 1, item2)
            item3 = QTableWidgetItem("GPU 每流处理器核心数")
            item3.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 2, item3)
            item4 = QTableWidgetItem("GPU 每流处理器最大线程块数")
            item4.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 3, item4)
            item5 = QTableWidgetItem("GPU 核心FLOPs")
            item5.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 4, item5)
            item6 = QTableWidgetItem("GPU 显存")
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

    def __initJobInfo(self, job, ifTrueJob=True):
        if ifTrueJob:
            self.nowJob = job
        else:
            self.nowJob = None
        self.jobInfoPage.jobName.setText(job.name)
        self.jobInfoPage.ram.setText(str(job.cpu_task.ram))
        self.jobInfoPage.period.setText(str(job.period))
        self.jobInfoPage.corenum.setValue(job.cpu_task.pes_number)
        self.jobInfoPage.cpuflops.setText(str(job.cpu_task.length))
        self._ui.homeui.tabWidget.setCurrentIndex(1)

    def _initKernelTable(self, kernel_num, kernel_infos):
        self.jobInfoPage.
        self.jobInfoPage.kernelTable.setRowCount(kernel_num + 1)
        # 设置不可见
        self.jobInfoPage.kernelTable.verticalHeader().setVisible(False)
        self.jobInfoPage.kernelTable.horizontalHeader().setVisible(False)
        i = 0
        item1 = QTableWidgetItem("Kernel ID")
        item1.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.kernelTable.setItem(i, 0, item1)
        item2 = QTableWidgetItem("Kernel 核心数")
        item2.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.kernelTable.setItem(i, 1, item2)
        item3 = QTableWidgetItem("Kernel 每流处理器核心数")
        item3.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.kernelTable.setItem(i, 2, item3)
        item4 = QTableWidgetItem("Kernel 核心FLOPs")
        item4.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.kernelTable.setItem(i, 3, item4)
        for kernel_info in kernel_infos:
            i += 1
            self.jobInfoPage.kernelTable.setItem(i, 0, QTableWidgetItem(str(i)))
            self.jobInfoPage.kernelTable.setItem(i, 1, QTableWidgetItem(str(kernel_info.cores)))
            self.jobInfoPage.kernelTable.setItem(i, 2, QTableWidgetItem(str(kernel_info.core_per_sm)))
            self.jobInfoPage.kernelTable.setItem(i, 3, QTableWidgetItem(str(kernel_info.flops_per_core)))
            del_kernel = QPushButton()
            del_kernel.setText("删除")
            del_kernel.clicked.connect(self._delKernel)
            self.jobInfoPage.kernelTable.setCellWidget(i, 4, del_kernel)

    def _initFaultInfo(self, fault: FaultGenerator, ifTrueFault=True):
        if ifTrueFault:
            self.nowFault = fault
        else:
            self.nowFault = None
        self.faultInfoPage.aim.addItems(sysSim.hosts.keys())
        self.faultInfoPage.name.setText(fault.name)
        self.faultInfoPage.aim.setCurrentText(fault.aim)
        self.faultInfoPage.type.setCurrentText(tranFromE2C(fault.mttf_type))
        print(tranFromE2C(fault.mttf_type))
        self.faultInfoPage.time1.setText(str(fault.mttf_scale))
        self.faultInfoPage.time2.setText(str(fault.mttr_scale))
        self._ui.homeui.tabWidget.setCurrentIndex(2)
        self._getNormalLine(fault.mttf_scale, fault.mttr_scale)


    def _getNormalLine(self, avg, avg2):
        print(avg)
        print(avg2)
        self.chart = QChart()
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
        self.chart.addSeries(self.series)

        rng2 = np.random.default_rng()
        data2 = rng2.normal(avg2, 1, 200000) 
        res_freq2 = stats.relfreq(data2, numbins=100)
        pdf_value2 = res_freq2.frequency
        x2 = res_freq2.lowerlimit + np.linspace(0, res_freq2.binsize * res_freq2.frequency.size, res_freq2.frequency.size)
        self.series2=QLineSeries()
        self.series2.setName("平均故障修复时间分布")
        # 填充QLineSeries
        for i in range(len(x2)):
                self.series2.append(x2[i],pdf_value2[i])
        self.chart.addSeries(self.series2)
        # 设置x坐标
        self.axis_x=QValueAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setLabelFormat("%.2f")
        self.axis_x.setTitleText("值(秒)")

        self.chart.addAxis(self.axis_x,Qt.AlignBottom) # 在表格中加入坐标，位置为底部
        self.series.attachAxis(self.axis_x) # 自动让QLineSeries贴附

        # 设置y坐标
        self.axis_y=QValueAxis()
        self.axis_y.setTickCount(10)
        self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setTitleText("概率")
        self.chart.addAxis(self.axis_y,Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.faultInfoPage.show.setChart(self.chart)
       

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
            self._ui.homeui.tabWidget.setCurrentIndex
            fault = FaultGenerator("正态分布", 0, 0)
            fault.setAim(sysSim.hosts.keys()[0])
            fault.setName("")
            self._initFaultInfo(FaultGenerator("正态分布", 0, 0), False)
        self.nowClect.removeChild(self._ui.homeui.infoList.currentItem())
    
    def _run(self):
        self._ui.central_window.centralWidget().setEnabled(False)
        self._ui.action_enable.setEnabled(True)
        self._ui.action_disable.setEnabled(False)

    def _initResult(self):
        # 绘制折线图
        path = "project/output/hostUtils.xml"
        xmlParser = XmlParser(path)
        self.cluster_result = xmlParser.parseHostRecord()
        path = "project/output/jobRun.xml"
        xmlParser = XmlParser(path)
        self.job_results = xmlParser.parseJobRecord()
        path = "project/output/faultRecords.xml"
        xmlParser = XmlParser(path)
        self.fault_results = xmlParser.parseFaultRecord()
        self.reliable = xmlParser.parseReliabilityRecord()
        remainAngle = (1.0 - self.reliable) * 360
        halfRemainAngle = remainAngle / 2
        startAngle = halfRemainAngle
        endAngle = 360 - halfRemainAngle
        self.pieSeries = QPieSeries()
        self.pieSeries.append("余度可靠性:" + str(self.reliable * 100) + "%", self.reliable * 100)
        self.pieSeries.append(":" + str((1 - self.reliable) * 100) + "%", (1 - self.reliable) * 100)
        self.pieSeries.setPieSize(0.5)
        # self.pieSeries.setPieStartAngle(startAngle)
        # self.pieSeries.setPieEndAngle(endAngle)

        chart = QChart()
        chart.addSeries(self.pieSeries)
        chart.setTitle("余度可靠性:" + str(self.reliable * 100) + "%")
        chart.legend().hide()
        self._ui.resultui.faultResultAnalysis.setChart(chart)
        # 抗锯齿
        self._ui.resultui.faultResultAnalysis.setRenderHint(QPainter.Antialiasing)
        self._ui.resultui.faultResultAnalysis.setRenderHint(QPainter.TextAntialiasing)

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
        self.jobRunTable.setRowCount(0)
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
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):  # Enable High DPI display with Qt5
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    QDir.addSearchPath("icons", f"{get_project_root_path().as_posix()}/widget_gallery/ui/svg")
    win = JobSimQt()
    win.menuBar().setNativeMenuBar(False)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    win.show()
    app.exec()
