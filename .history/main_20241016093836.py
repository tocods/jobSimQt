# ---------------------------------------------------------------------------------------------
#  Copyright (c) Yunosuke Ohsugi. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------*/

import sys
import random
import qdarktheme
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot
from qdarktheme.qtpy.QtGui import *
from qdarktheme.qtpy.QtWidgets import *
from qdarktheme.util import get_project_root_path
from main_ui import UI
from util.jobSim import sysSim, ParseUtil, HostInfo, CPUInfo, GPUInfo
from jobSimPage import JobSimPage
from component.hostinfo import Ui_HostInfo
from component.jobinfo import Ui_JobInfo


class JobSimQt(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
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
        path = "project/hosts.json"
        parser = ParseUtil()
        self.hosts = parser.parseHosts(path)
        print(self.hosts)
        for host in self.hosts:
            sysSim.hosts[host.name] = host
        path = "project/jobs.json"
        self.jobs = parser.parseJobs(path)
        sysSim.jobs = self.jobs
        path = "project/faults.json"
        self.faults = parser.parseFaults(path)
        sysSim.faults = self.faults

        w = QWidget()
        self.hostInfoPage = Ui_HostInfo()
        self.hostInfoPage.setupUi(w)
        self.hostInfoPage.pushButton.setIcon(QIcon("img/加.png"))
        self._ui.homeui.tabWidget.addTab(w, "主机")
        screesize = self._ui.homeui.tabWidget.size()
        w.setGeometry(0, 0, screesize.width(), screesize.height())

        j = QWidget()
        self.jobInfoPage = Ui_JobInfo()
        self.jobInfoPage.setupUi(j)
        self.jobInfoPage.pushButton.setIcon(QIcon("img/加.png"))
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
        #获取点击item所属根节点的名称（如无根节点则返回自身）
        self.nowClect = self._ui.homeui.infoList.currentItem().parent()
        if self.nowClect is None:
            self.nowClect = self._ui.homeui.infoList.currentItem()
        print(self.nowClect.text(0))
        if self.nowClect.text(0) == '主机':
            host = sysSim.hosts[self._ui.homeui.infoList.currentItem().text(0)]
            self._initHostInfo(host)
        elif self.nowClect.text(0) == '任务':
            for job in self.jobs:
                if job.name == self._ui.homeui.infoList.currentItem().text(0):
                   self.__initJobInfo(job)

    def _add(self):
        print("add aa")
        if self.nowClect is None:
            return
        print("add")
        r = random.randint(0, 100)
        item = QTreeWidgetItem([f"{self.nowClect}新增"])
        self.nowClect.addChild(item)
        

    def _initHostInfo(self, host: HostInfo):
        self.hostInfoPage.hostName.setText(host.name)
        self.hostInfoPage.ram.setValue(host.ram)
        cpunum = len(host.cpu_infos)
        cpucore = cpunum * host.cpu_infos[0].cores
        self.hostInfoPage.corenum.setValue(cpucore)
        self.hostInfoPage.cpunum.setValue(cpunum)
        self.hostInfoPage.cpuflops.setText(str(host.cpu_infos[0].mips))
        self._ui.homeui.tabWidget.setCurrentIndex(0)

    def __initJobInfo(self, job):
        self.jobInfoPage.jobName.setText(job.name)
        self.jobInfoPage.ram.setText(str(job.cpu_task.ram))
        self.jobInfoPage.period.setText(str(job.period))
        self.jobInfoPage.corenum.setValue(job.cpu_task.pes_number)
        self.jobInfoPage.cpuflops.setText(str(job.cpu_task.length))
        self._ui.homeui.tabWidget.setCurrentIndex(1)


    def _delete(self):
        print("delete")
        if self.nowClect is None:
            return
        self.nowClect.parent().removeChild(self.nowClect)
    
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
