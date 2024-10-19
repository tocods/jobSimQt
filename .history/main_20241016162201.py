# ---------------------------------------------------------------------------------------------
#  Copyright (c) Yunosuke Ohsugi. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------*/

import sys
import random
from functools import partial
import qdarktheme
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot
from qdarktheme.qtpy.QtGui import *
from qdarktheme.qtpy.QtWidgets import *
from qdarktheme.util import get_project_root_path
from main_ui import UI
from util.jobSim import sysSim, ParseUtil, HostInfo, CPUInfo, GPUInfo, VideoCardInfo, JobInfo, CPUTaskInfo, GPUTaskInfo
from jobSimPage import JobSimPage
from component.hostinfo import Ui_HostInfo
from component.jobinfo import Ui_JobInfo


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
            item = QTreeWidgetItem([fault.aim])
            itemfault.addChild(item)
        self._ui.homeui.infoList.clicked.connect(self._showInfo)
        self._ui.homeui.infoList.setHeaderHidden(True)
        self.setGeometry(0, 0, screen_size.width() * 0.9, screen_size.height() * 0.9)
        self._ui.homeui.widget.setGeometry(0, 0, screen_size.width() * 0.7, screen_size.height() * 0.7)
    


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
        # 更新树
        for i in range(self.nowClect.childCount()):
            if self.nowClect.child(i).text(0) == name_before:
                self.nowClect.child(i).setText(0, self.nowJob.name)
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
        self.hostInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
        self.hostInfoPage.gputable.setItem(i, 1, QTableWidgetItem("0"))
        self.hostInfoPage.gputable.setItem(i, 2, QTableWidgetItem("0"))
        self.hostInfoPage.gputable.setItem(i, 3, QTableWidgetItem("0"))
        self.hostInfoPage.gputable.setItem(i, 4, QTableWidgetItem("0"))
        

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
        self.nowClect.removeChild(self._ui.homeui.infoList.currentItem())
    
    def _run(self):
        self._ui.central_window.centralWidget().setEnabled(False)
        self._ui.action_enable.setEnabled(True)
        self._ui.action_disable.setEnabled(False)

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
