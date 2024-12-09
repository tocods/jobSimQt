from qdarktheme.qtpy.QtGui import QMouseEvent
from Window.EditHostNetargsWindow import *
from Window.EditLinkArgsWindow import EditLinkArgsWindow
from Window.EditSwitchNetargsWindow import *
from component.jobinfo import Ui_JobInfo
from component.hostinfo import Ui_HostInfo
from component.faultinfo import Ui_FaultInfo
import globaldata
import os
from qdarktheme.qtpy.QtWidgets import (
    QWidget,
    QGraphicsView,
    QMenu,
    QGraphicsPathItem,
    QGraphicsItemGroup,
    QGraphicsSceneMouseEvent,
    QHBoxLayout,
    QTableWidget,
    QComboBox,
)
import numpy as np
from scipy import stats
import os
from qdarktheme.qtpy.QtCore import Qt, QRect, QRegularExpression
from qdarktheme.qtpy.QtGui import QPainter, QAction, QCursor, QIcon, QFont, QColor, QRegularExpressionValidator
from PySide6.QtCharts import QChart,QChartView,QLineSeries,QDateTimeAxis,QValueAxis, QPieSeries
from util.table import NumericDelegate
from item import GraphicItem, HostGraphicItem, SwitchGraphicItem
from edge import Edge, GraphicEdge
from HostInfoForm import HostInfoForm
from HostInfoForm import HostInfoForm
from util.jobSim import sysSim, HostInfo, JobInfo, CPUInfo, GPUInfo, VideoCardInfo, GPUTaskInfo, CPUTaskInfo, FaultGenerator, tranFromC2E, tranFromE2C
from entity.host import *
from entity.switch import *
from jobSimPainter import Painter, XmlParser
import random

class GraphicView(QGraphicsView):

    def __init__(self, graphic_scene, parent=None):
        super().__init__(parent)
        self.master = False
        self.jobSim = sysSim
        self.gr_scene = graphic_scene
        self.parent = parent
        self.drag_start_item = None
        # item menu
        self.item_clicked = None
        self.menu = QMenu(self)
        self.setFault = QAction(text="注入故障")
        self.deleteAction = QAction(text="删除")
        self.setJob = QAction(text="添加软件")
        self.sCalculation = QAction(text="设置计算属性")
        self.sMaster = QAction(text="设为主节点")
        self.deleteAction.triggered.connect(self.deleteItem)
        self.setJob.triggered.connect(self.addJob)
        self.sCalculation.triggered.connect(self.setCalculation)
        self.setFault.triggered.connect(self.addFault)
        self.sMaster.triggered.connect(self.setMaster)
        self.names = []
        self.hostInform = HostInfoForm(self.jobSim)
        self.init_ui()

        self.lineToolEnabled = False
        self.hostAdding = False
        self.switchAdding = False

        self.parent.ui.infoList.clicked.connect(self._showInfo)

    def init_ui(self):
        self.setScene(self.gr_scene)
        # 设置渲染属性
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing
            |
            # QPainter.RenderHint.HighQualityAntialiasing |
            QPainter.RenderHint.TextAntialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
            | QPainter.RenderHint.LosslessImageRendering
        )
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        # 设置水平和竖直方向的滚动条显示
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        # 设置拖拽模式
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def setHostToAdd(
        self, host_name, host_type, img, width, height, onlyCpu, Host_class
    ):
        self.lineToolDisable()
        self.hostAdding = True
        self.hostToAdd_name = host_name
        self.hostToAdd_type = host_type
        self.hostToAdd_img = img
        self.hostToAdd_width = width
        self.hostToAdd_height = height
        self.hostToAdd_onlyCpu = onlyCpu
        self.hostToAdd_class = Host_class

    # 在画布上添加主机
    def createGraphicHostItem(
        self,
        host_name,
        host_type,
        img,
        width,
        height,
        onlyCpu=False,
        Host_class=Host,
        pos_x=0,
        pos_y=0,
    ):
        item = HostGraphicItem(
            host_name, host_type, img, width, height, parent=self, Host_class=Host_class
        )
        # new_host = HostInfo(host_name, [], [CPUInfo(2, 1000)], 4)
        # sysSim.hosts[host_name] = new_host
        # 将onlyCpu记录到属性中
        item.hostAttr.only_cpu = onlyCpu
        item.setPos(pos_x, pos_y)
        self.jobSim.addHostItem(item, onlyCPU=onlyCpu)
        self.gr_scene.add_node(item)
        return item

    def setSwitchToAdd(
        self, switch_name, switch_type, img, width, height, Switch_class
    ):
        self.lineToolDisable()
        self.switchAdding = True
        self.switchToAdd_name = switch_name
        self.switchToAdd_type = switch_type
        self.switchToAdd_img = img
        self.switchToAdd_width = width
        self.switchToAdd_height = height
        self.switchToAdd_class = Switch_class

    def stopAdding(self):
        self.hostAdding = False
        self.switchAdding = False

    # 在画布上添加交换机
    def createGraphicSwitchItem(
        self,
        switch_name,
        switch_type,
        img,
        width,
        height,
        Switch_class=Switch,
        pos_x=0,
        pos_y=0,
    ):
        item = SwitchGraphicItem(
            switch_name,
            switch_type,
            img,
            width,
            height,
            parent=self,
            Switch_class=Switch_class,
        )
        item.setPos(pos_x, pos_y)
        self.gr_scene.add_node(item)
        return item

    # 在画布上添加连接
    def createGraphicLink(self, endpoint1, endpoint2):
        new_edge = Edge(self.gr_scene, endpoint1, endpoint2)
        # 保存连接线
        new_edge.store()

        return new_edge

    def keyPressEvent(self, event):
        # 新建图元样例，可忽略
        if event.key() == Qt.Key.Key_N:
            event.ignore()  # 忽略默认行为
            self.createGraphicHostItem("Model.png")
        else:
            super().keyPressEvent(event)

    def openHostEditor(self, item):
        if isinstance(item.hostAttr, NormalHost):
            self.editHostNetargsWindowNormal.setHostGraphicItem(item)
            self.editHostNetargsWindowNormal.show()
        if isinstance(item.hostAttr, UdpHost):
            self.editHostNetargsWindowUdp.setHostGraphicItem(item)
            self.editHostNetargsWindowUdp.show()
        if isinstance(item.hostAttr, TsnHost):
            self.editHostNetargsWindowTsn.setHostGraphicItem(item)
            self.editHostNetargsWindowTsn.show()
        if isinstance(item.hostAttr, TcpHost):
            self.editHostNetargsWindowTcp.setHostGraphicItem(item)
            self.editHostNetargsWindowTcp.show()
        if isinstance(item.hostAttr, DdsHost):
            self.editHostNetargsWindowDds.setHostGraphicItem(item)
            self.editHostNetargsWindowDds.show()
        if isinstance(item.hostAttr, RdmaHost):
            self.editHostNetargsWindowRdma.setHostGraphicItem(item)
            self.editHostNetargsWindowRdma.show()

    def graphicItemClicked(self, item, event: QGraphicsSceneMouseEvent):
        self.item_clicked = item
        self.menu = QMenu(self)
        if isinstance(self.item_clicked, HostGraphicItem):
            name = item.hostAttr.name
            host = sysSim.hosts[name]
            if host.ifMaster:
                self.sMaster.setText("设为从节点")
            else:
                self.sMaster.setText("设为主节点")
            self.menu.addAction(self.sMaster)
            self.menu.addAction(self.sCalculation)
            self.menu.addAction(self.setJob)
            self.menu.addAction(self.setFault)
            self.menu.addAction(self.deleteAction)
            self.parent.selectHost(item)
        if isinstance(self.item_clicked, SwitchGraphicItem):
            self.parent.selectSwitch(item)
            self.menu.addAction(self.deleteAction)
        if event.button() == Qt.MouseButton.RightButton:
            print("右键")
            print(item.name)
            self.menu.popup(QCursor.pos())
        elif self.lineToolEnabled:
            self.lineClick()

    def linkClicked(self, link, event: QGraphicsSceneMouseEvent):
        self.item_clicked = link
        self.parent.selectLink(link)
        if event.button() == Qt.MouseButton.RightButton:
            self.menu.popup(QCursor.pos())
        return

    # 获取点击的link
    def get_link_at_pos(self, event):
        pos = event.pos()
        # item = self.itemAt(pos)
        """ 鼠标所在的10*10内都是选中范围 """
        area = QRect(pos.x() - 5, pos.y() - 5, 10, 10)
        if len(self.items(area)) == 0:
            return None
        result = self.items(area)[0]
        # if result.type() == GraphicItem.type or result.type() == QGraphicsPathItem
        if isinstance(result, QGraphicsPathItem):
            return result
        else:
            return None

    def get_items_at_rubber(self):
        """Get group select items."""
        area = self.rubberBandRect()
        return self.items(area)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            targetPos = self.mapToScene(event.pos())
            if self.hostAdding:
                self.createGraphicHostItem(
                    self.hostToAdd_name,
                    self.hostToAdd_type,
                    self.hostToAdd_img,
                    self.hostToAdd_width,
                    self.hostToAdd_height,
                    self.hostToAdd_onlyCpu,
                    self.hostToAdd_class,
                    targetPos.x(),
                    targetPos.y(),
                )
            elif self.switchAdding:
                self.createGraphicSwitchItem(
                    self.switchToAdd_name,
                    self.switchToAdd_type,
                    self.switchToAdd_img,
                    self.switchToAdd_width,
                    self.switchToAdd_height,
                    self.switchToAdd_class,
                    targetPos.x(),
                    targetPos.y(),
                )
        link = self.get_link_at_pos(event)
        if link != None:
            self.linkClicked(link, event)
        self.parent.update_tree_view()

    def lineToolStateChange(self):
        if not self.lineToolEnabled:
            self.lineToolEnable()
        else:
            self.lineToolDisable()

    def lineToolEnable(self):
        self.lineToolEnabled = True
        self.parent.ui.add_line.setText("停止连线")
        self.hostAdding = False
        self.switchAdding = False

    def lineToolDisable(self):
        self.lineToolEnabled = False
        self.parent.ui.add_line.setText("连线")

    def lineClick(self):
        item = self.item_clicked
        if isinstance(item, GraphicItem):
            # 是起点
            if self.drag_start_item == None:
                self.drag_start_item = item
            # 是终点
            else:
                # 终点图元不能是起点图元，即无环图
                if item is not self.drag_start_item:
                    # 检查是否已经存在一条线
                    existed = False
                    for link in globaldata.linkList:
                        if (
                            link.start_item == self.drag_start_item
                            and link.end_item == item
                            or link.end_item == self.drag_start_item
                            and link.start_item == item
                        ):
                            existed = True
                    if not existed:
                        new_edge = Edge(self.gr_scene, self.drag_start_item, item)
                        # 保存连接线
                        new_edge.store()
                        self.drag_start_item = None
                        # self.lineToolEnable()
                else:
                    self.drag_start_item = None

        globaldata.calculate_link_port()

    def deleteItem(self):
        # 删除键
        item = self.item_clicked
        if isinstance(item, QGraphicsItemGroup):
            self.gr_scene.remove_node(item)
            sysSim.hosts.pop(item.hostAttr.name)
            # 遍历任务
            for name in sysSim.jobs:
                job = sysSim.jobs[name]
                if job.host == item.hostAttr.name:
                    sysSim.jobs.pop(name)
            for name in sysSim.faults:
                fault = sysSim.faults[name]
                if fault.aim == item.hostAttr.name:
                    sysSim.faults.pop(name)
            sysSim.manager.pop(item.hostAttr.name)
            self.gr_scene.remove_node(item)
        if isinstance(item, QGraphicsPathItem):
            self.gr_scene.remove_edge(item)
        self.parent.cancelSelect()
        self.parent.update_tree_view()

    # def mouseReleaseEvent(self, event):
    #         super().mouseReleaseEvent(event)

    def addJob(self):
        self.sJMain = QWidget()
        screen_size = sysSim.screenSize
        self.sJMain.setGeometry(screen_size.width() * 0.3, screen_size.height() * 0.3, screen_size.width() * 0.5, screen_size.height() * 0.5)
        # self.sJMain.center()
        self.sJMain.setWindowTitle("设置软件属性")
        self.sJMain.setWindowIcon(QIcon("img/仿真.png"))
        hL = QHBoxLayout()
        self.sJMain.setLayout(hL)
        self.sJTab = QTabWidget(self.sJMain)
        hL.addWidget(self.sJTab)
        self.sJ = QWidget()
        self.jobInfoPage = Ui_JobInfo()
        self.jobInfoPage.setupUi(self.sJ)
        #self.sJ.setGeometry(screen_size.width() * 0.3, screen_size.width() * 0.3, screen_size.width() * 0.5, screen_size.height() * 0.5)
        self.sJTab.addTab(self.sJ, "计算信息")
        self.hostApp = HostNetargsAppEditorApp("", True)
        self.sJTab.addTab(self.hostApp, "网络流")
        self.hostMiddleware = HostNetargsAppEditorMiddleware("", True)
        self.sJTab.addTab(self.hostMiddleware, "网络中间件")

        r = random.randint(0, 10000)
        name = "软件" + f"_{r}"
        while name in sysSim.jobs:
            r = random.randint(0, 10000)
            name = "软件" + f"_{r}"
        k = GPUTaskInfo.Kernel(0, 1, 10, 0, 0, 0, 'CPU')
        new_job = JobInfo(name, 10, CPUTaskInfo(100, 1, 1000), GPUTaskInfo([k]))
        new_job.setDeadline(5)
        new_job.setHost(self.item_clicked.hostAttr.name)
        sysSim.jobs[name] = new_job
        self.nowJob = new_job
        self.jobInfoPage.pushButton.setIcon(QIcon("img/加.png"))
        self.jobInfoPage.apply.clicked.connect(self._applyJob)
        self.jobInfoPage.delete_2.clicked.connect(self._delJob)
        self.addJobMenu = QMenu(self)
        self.cpuAc = QAction("CPU运行")
        self.gpuAc = QAction("GPU运行")
        #self.cpuAc.triggered.connect(self._cpuRun)
        self.gpuAc.triggered.connect(self._addKernel)
        self.cpuAc.triggered.connect(self._addCpuKernel)
        self.addJobMenu.addAction(self.cpuAc)
        self.addJobMenu.addAction(self.gpuAc)
        self.jobInfoPage.pushButton.setMenu(self.addJobMenu)
        self.__initJobInfo(new_job)
        self.parent.update_tree_view()
        self.sJMain.show()
    
    def setCalculation(self):
        self.sH = QWidget()
        screen_size = sysSim.screenSize
        self.sH.setWindowIcon(QIcon("img/仿真.png"))
        self.hostInfoPage = Ui_HostInfo()
        self.hostInfoPage.setupUi(self.sH)
        self.sH.setWindowTitle("设置计算属性")
        self.sH.setGeometry(screen_size.width() * 0.3, screen_size.height() * 0.3, screen_size.width() * 0.5, screen_size.height() * 0.5)
        host = self.item_clicked.hostAttr.name
        host = sysSim.hosts[host]
        self.nowHost = host
        self.hostInfoPage.pushButton.setIcon(QIcon("img/加.png"))
        self.hostInfoPage.apply.clicked.connect(self._applyHost)
        self.hostInfoPage.pushButton.clicked.connect(self._addGpu)
        self._initHostInfo(host)
        self.sH.show()

    def addFault(self):
        host = self.item_clicked.hostAttr.name
        self.faultInfoPage = Ui_FaultInfo()
        self.sF = QWidget()
        self.faultInfoPage.setupUi(self.sF)
        r = random.randint(0, 10000)
        name = "故障" + f"_{r}"
        while name in sysSim.faults:
            r = random.randint(0, 10000)
            name = "故障" + f"_{r}"
        new_fault = FaultGenerator("Normal", 10, 10)
        new_fault.setAim(host)
        new_fault.setName(name)
        new_fault.setHardware("CPU")
        sysSim.faults[name] = new_fault
        self.nowFault = new_fault
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
        self._initFaultInfo(new_fault)
        screen_size = sysSim.screenSize
        self.sF.setGeometry(0, 0, screen_size.width() * 0.4, screen_size.height() * 0.4)
        self.sF.setWindowIcon(QIcon("img/仿真.png"))
        self.sF.setWindowTitle("设置故障属性")
        self.sF.setGeometry(screen_size.width() * 0.3, screen_size.height() * 0.3, screen_size.width() * 0.5, screen_size.height() * 0.5)
        self.parent.update_tree_view()
        self.sF.show()

    def setMaster(self):
        host = self.item_clicked.hostAttr.name
        hostChose = sysSim.hosts[host]
        if not hostChose.ifMaster:
            hostChose.ifMaster = True
            #self.sMaster.setText("设为从节点")
            manager = sysSim.manager[host]
            manager.name = "系统管理软件(主)"
            sysSim.manager[host] = manager
            self.parent.update_tree_view()
        else:
            hostChose.ifMaster = False
            #self.sMaster.setText("设为主节点")
            manager = sysSim.manager[host]
            manager.name = "系统管理软件"
            sysSim.manager[host] = manager
            self.parent.update_tree_view()

    def _initHostInfo(self, host: HostInfo, ifTrueHost=True):
        self.gpu_num = 0
        self.cpushow = QChartView()
        self.ramshow = QChartView()
        self.gpushow = QChartView()
        self.cpushow.setChart(QChart())
        self.ramshow.setChart(QChart())
        self.gpushow.setChart(QChart())
        if ifTrueHost:
            self.nowHost = host
        else:
            self.nowHost = None
        if ifTrueHost and os.path.isdir(sysSim.path + "/OutputFiles") and os.path.isfile(sysSim.path + "/OutputFiles/hostUtils.xml"):
            path = sysSim.path + "/OutputFiles/hostUtils.xml"
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
        self.hostInfoPage.shows.clear()
        self.hostInfoPage.shows.addTab(self.cpushow, "CPU利用率")
        self.hostInfoPage.shows.addTab(self.ramshow, "内存利用率")
        self.hostInfoPage.shows.addTab(self.gpushow, "GPU利用率")
        self.hostInfoPage.hostName.setText(host.name)
        self.hostInfoPage.ram.setValue(host.ram)
        cpunum = len(host.cpu_infos)
        cpucore = host.cpu_infos[0].cores
        self.hostInfoPage.corenum.setValue(cpucore)
        self.hostInfoPage.cpunum.setValue(cpunum)
        self.hostInfoPage.cpuflops.setText(str(host.cpu_infos[0].mips))
        self.hostInfoPage.lineEdit.setText(str(host.cpu_infos[0].int_mips))
        self.hostInfoPage.lineEdit_2.setText(str(host.cpu_infos[0].matrix_mips))
        # 设置正则表达式为运行2位小鼠数
        reg_ex =  QRegularExpression("^([0-9]{1,}[.]{0,1}[0-9]{0,2})$")
        validator = QRegularExpressionValidator(reg_ex, self.hostInfoPage.cpuflops)
        self.hostInfoPage.cpuflops.setValidator(validator)
        if host.video_card_infos != []:
            print(host.video_card_infos[0].pcie_bw)
            self.hostInfoPage.pcie.setValue(host.video_card_infos[0].pcie_bw)
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
        f = QFont()
        f.setPointSize(10)
        self.hostInfoPage.gputable.setFont(f)
        delegate = NumericDelegate(self.hostInfoPage.gputable)
        self.hostInfoPage.gputable.setItemDelegate(delegate)
        self.hostInfoPage.gputable.setColumnCount(9)
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
        item4 = QTableWidgetItem("SM最大线程块")
        item4.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 3, item4)
        item5 = QTableWidgetItem("浮点计算能力")
        item5.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 4, item5)
        item6 = QTableWidgetItem("整数计算能力")
        item6.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 5, item6)
        item7 = QTableWidgetItem("矩阵运算能力")
        item7.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 6, item7)
        item8 = QTableWidgetItem("显存(GB)")
        item8.setBackground(QColor(192, 192, 192))
        self.hostInfoPage.gputable.setItem(i, 7, item8)

        for gpu_info in gpu_infos:
            i += 1
            self.hostInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
            self.hostInfoPage.gputable.setItem(i, 1, QTableWidgetItem(str(gpu_info.cores)))
            self.hostInfoPage.gputable.setItem(i, 2, QTableWidgetItem(str(gpu_info.core_per_sm)))
            self.hostInfoPage.gputable.setItem(i, 3, QTableWidgetItem(str(gpu_info.max_block_per_sm))
            )
            self.hostInfoPage.gputable.setItem(i, 4, QTableWidgetItem(str(gpu_info.flops_per_core)))
            self.hostInfoPage.gputable.setItem(i, 5, QTableWidgetItem(str(gpu_info.int_flops_per_core)))
            self.hostInfoPage.gputable.setItem(i, 6, QTableWidgetItem(str(gpu_info.matrix_flops_per_core)))
            self.hostInfoPage.gputable.setItem(i, 7, QTableWidgetItem(str(gpu_info.gddram)))
            del_gpu = QPushButton()
            del_gpu.setText("删除")
            del_gpu.clicked.connect(self._delGpu)
            self.hostInfoPage.gputable.setCellWidget(i, 8, del_gpu)

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
            self.hostInfoPage.gputable.setColumnCount(9)
            item1 = QTableWidgetItem("GPU ID")
            item1.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 0, item1)
            item2 = QTableWidgetItem("核心数")
            item2.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 1, item2)
            item3 = QTableWidgetItem("SM核心数")
            item3.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 2, item3)
            item4 = QTableWidgetItem("SM最大线程块")
            item4.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 3, item4)
            item5 = QTableWidgetItem("浮点计算能力")
            item5.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 4, item5)
            item6 = QTableWidgetItem("整数计算能力")
            item6.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 5, item6)
            item7 = QTableWidgetItem("矩阵运算能力")
            item7.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 6, item7)
            item8 = QTableWidgetItem("显存(GB)")
            item8.setBackground(QColor(192, 192, 192))
            self.hostInfoPage.gputable.setItem(0, 7, item8)

        self.hostInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
        self.hostInfoPage.gputable.setItem(i, 1, QTableWidgetItem("1000"))
        self.hostInfoPage.gputable.setItem(i, 2, QTableWidgetItem("100"))
        self.hostInfoPage.gputable.setItem(i, 3, QTableWidgetItem("10"))
        self.hostInfoPage.gputable.setItem(i, 4, QTableWidgetItem("10"))
        self.hostInfoPage.gputable.setItem(i, 5, QTableWidgetItem("10"))
        self.hostInfoPage.gputable.setItem(i, 6, QTableWidgetItem("10"))
        self.hostInfoPage.gputable.setItem(i, 7, QTableWidgetItem("10"))
        del_gpu = QPushButton()
        del_gpu.setText("删除")
        del_gpu.clicked.connect(self._delGpu)
        self.hostInfoPage.gputable.setCellWidget(i, 8, del_gpu)

    def _applyHost(self):
        print("apply host")
        if self.hostInfoPage.hostName.text() == "":
            QMessageBox.information(self, "错误", "主机名不能为空")
            self._initHostInfo(self.nowHost)
            return
        if self.hostInfoPage.hostName.text() in sysSim.hosts and self.hostInfoPage.hostName.text() != self.nowHost.name:
            QMessageBox.information(self, "错误", "主机名重复")
            self._initHostInfo(self.nowHost)
            return
        if self.hostInfoPage.ram.text() == "" or int(self.hostInfoPage.ram.value()) == 0:
            QMessageBox.information(self, "错误", "主机内存不能为0")
            self._initHostInfo(self.nowHost)
            return
        if self.hostInfoPage.cpunum.text() == "" or int(self.hostInfoPage.cpunum.value()) == 0:
            print("asa")
            QMessageBox.information(self, "错误", "主机CPU数不能为0")
            self._initHostInfo(self.nowHost)
            return
        if self.hostInfoPage.corenum.text() == "" or int(self.hostInfoPage.corenum.value()) == 0:
            QMessageBox.information(self, "错误", "主机CPU核数不能为0")
            self._initHostInfo(self.nowHost)
            return
        if self.hostInfoPage.cpuflops.text() == "" or float(self.hostInfoPage.cpuflops.text()) == 0.0:
            QMessageBox.information(self, "错误", "主机核FLOPs不能为0")
            self._initHostInfo(self.nowHost)
            return
        name_before = self.nowHost.name
        self.nowHost.name = self.hostInfoPage.hostName.text()
        self.nowHost.ram = self.hostInfoPage.ram.value()
        cpunum = self.hostInfoPage.cpunum.value()
        cpucore = self.hostInfoPage.corenum.value()
        cpuflops = self.hostInfoPage.cpuflops.text()
        cpuintflops = self.hostInfoPage.lineEdit.text()
        cpumatrixflops = self.hostInfoPage.lineEdit_2.text()
        self.nowHost.cpu_infos = []
        for i in range(cpunum):
            self.nowHost.cpu_infos.append(CPUInfo(cpucore, cpuflops, cpuintflops, cpumatrixflops))
        self.nowHost.video_card_infos = []
        # 更新GPU
        if self.gpu_num > 0:
            self.nowHost.video_card_infos = []
            gpus = []
            for i in range(self.hostInfoPage.gputable.rowCount() - 1):
                n = i + 1
                n = n.__str__()
                if int(self.hostInfoPage.gputable.item(i + 1, 1).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个GPU的核心数不能为0")
                    continue
                if int(self.hostInfoPage.gputable.item(i + 1, 2).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个GPU的每SM核心数不能为0")
                    continue
                if int(self.hostInfoPage.gputable.item(i + 1, 3).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个GPU的SM最大线程块数不能为0")
                    continue
                if int(self.hostInfoPage.gputable.item(i + 1, 4).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个GPU的核心浮点计算能力不能为0")
                    continue
                if int(self.hostInfoPage.gputable.item(i + 1, 5).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个GPU的核心整数计算能力不能为0")
                    continue
                if int(self.hostInfoPage.gputable.item(i + 1, 6).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个GPU的核心矩阵计算能力不能为0")
                    continue
                if int(self.hostInfoPage.gputable.item(i + 1, 7).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个GPU的显存不能为0")
                    continue
                gpu = GPUInfo(int(self.hostInfoPage.gputable.item(i + 1, 1).text()), (int)(self.hostInfoPage.gputable.item(i + 1, 2).text()), (int)(self.hostInfoPage.gputable.item(i+ 1, 3).text()), (int)(self.hostInfoPage.gputable.item(i+1, 7).text()), (int)(self.hostInfoPage.gputable.item(i+1, 4).text()), (int)(self.hostInfoPage.gputable.item(i+1, 5).text()), (int)(self.hostInfoPage.gputable.item(i+1, 6).text()))
                gpus.append(gpu)
            if len(gpus) > 0:
                videoCardInfo = VideoCardInfo(gpus)
                if (int)(self.hostInfoPage.pcie.value()) == 0:
                    QMessageBox.information(self, "错误", "PCIe带宽不能为0")
                    return
                videoCardInfo.pcie_bw = (int)(self.hostInfoPage.pcie.value()) 
                print("apply: " + videoCardInfo.pcie_bw.__str__())
                self.nowHost.video_card_infos.append(videoCardInfo)
        self.nowHost.print()
        sysSim.hosts.pop(name_before)
        sysSim.hosts[self.nowHost.name] = self.nowHost
        sysSim.manager[self.nowHost.name] = sysSim.manager[name_before]
        if name_before != self.nowHost.name:
            sysSim.manager.pop(name_before)
        for job in sysSim.jobs:
            if sysSim.jobs[job].host == name_before:
                sysSim.jobs[job].host = self.nowHost.name
        for fault in sysSim.faults:
            if sysSim.faults[fault].aim == name_before:
                sysSim.faults[fault].aim = self.nowHost.name
        self.parent.changeHostName(self.nowHost.name)
        self._initHostInfo(self.nowHost)
    
    def __initJobInfo(self, job: JobInfo, ifTrueJob=True):
        if ifTrueJob:
            self.nowJob = job
        else:
            self.nowJob = None
        if ifTrueJob and os.path.isdir(sysSim.path + "/OutputFiles") and os.path.isfile(sysSim.path + "/OutputFiles/jobRun.xml"):
            path = sysSim.path + "/OutputFiles/jobRun.xml"
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
        # self.jobInfoPage.corenum.setValue(job.cpu_task.pes_number)
        # self.jobInfoPage.cpuflops.setText(str(job.cpu_task.length))
        # reg_ex =  QRegularExpression("[0-9]+")
        # validator = QRegularExpressionValidator(reg_ex, self.jobInfoPage.cpuflops)
        # self.jobInfoPage.cpuflops.setValidator(validator)
        if job.gpu_task is not None:
            print("gpu task")
            self.kernel_num = len(job.gpu_task.kernels) - 1
            self._initKernelTable(self.kernel_num, job.gpu_task)
        else:
            print("no gpu task")
            self.kernel_num = 0
            self._initKernelTable(0, None)
        self.jobInfoPage.host.clear()
        self.jobInfoPage.host.addItem(job.host)
        self.jobInfoPage.host.setCurrentText(job.host)
        print(job.host)
        print("===")
        if job.host != "":
            self.jobInfoPage.host.setCurrentText(job.host)
        else:
            self.jobInfoPage.host.setCurrentText("不指定")
       

    def _initKernelTable(self, kernel_num, gpu_task):
        print("init kernel table, " + kernel_num.__str__())
        delegate = NumericDelegate(self.jobInfoPage.gputable)
        self.jobInfoPage.gputable.setItemDelegate(delegate)
        self.jobInfoPage.gputable.setColumnCount(10)
        self.jobInfoPage.gputable.setRowCount(2*(kernel_num + 1))
        # 设置不可见
        self.jobInfoPage.gputable.verticalHeader().setVisible(False)
        self.jobInfoPage.gputable.horizontalHeader().setVisible(False)
        i = 0
        item1 = QTableWidgetItem("顺序")
        item1.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 0, item1)
        item2 = QTableWidgetItem("硬件")
        item2.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 1, item2)
        item3 = QTableWidgetItem("线程数")
        item3.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 2, item3)
        item4 = QTableWidgetItem("GFLOPs")
        item4.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 3, item4)
        item5 = QTableWidgetItem("类型")
        item5.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 4, item5)
        i += 1
        cpuTask = gpu_task.kernels[0]
        print(cpuTask.hardware + "haha")
        self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(i)))
        self.jobInfoPage.gputable.setItem(i, 1, QTableWidgetItem(str(cpuTask.hardware)))
        self.jobInfoPage.gputable.setItem(i, 2, QTableWidgetItem(str(cpuTask.thread_num)))
        self.jobInfoPage.gputable.setItem(i, 3, QTableWidgetItem(str(cpuTask.thread_length)))
        combox = QComboBox()
        combox.addItem("整数")
        combox.addItem("浮点")
        combox.addItem("矩阵")
        combox.setCurrentText(cpuTask.type)
        self.jobInfoPage.gputable.setCellWidget(i, 4, combox)   
        if gpu_task is not None:
            first = True
            for kernel_info in gpu_task.kernels:
                if first:
                    first = False
                    continue
                if kernel_info.hardware == "CPU":
                    print("is cpu")
                    i += 1
                    item1 = QTableWidgetItem("顺序")
                    item1.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 0, item1)
                    itemx = QTableWidgetItem("硬件")
                    itemx.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 1, itemx)
                    item2 = QTableWidgetItem("线程数")
                    item2.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 2, item2)
                    item4 = QTableWidgetItem("GFLOPs")
                    item4.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 3, item4)
                    item8 = QTableWidgetItem("类型")
                    item8.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 4, item8)
                    i += 1
                    self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(int((i+1)/2))))
                    self.jobInfoPage.gputable.setItem(i, 1, QTableWidgetItem(str(kernel_info.hardware)))
                    self.jobInfoPage.gputable.setItem(i, 2, QTableWidgetItem(str(kernel_info.thread_num)))
                    self.jobInfoPage.gputable.setItem(i, 3, QTableWidgetItem(str(kernel_info.thread_length)))
                    typeChose = QComboBox()
                    typeChose.addItem("整数")
                    typeChose.addItem("浮点")
                    typeChose.addItem("矩阵")
                    typeChose.setCurrentText(kernel_info.type)
                    self.jobInfoPage.gputable.setCellWidget(i, 4, typeChose)
                    del_kernel = QPushButton()
                    del_kernel.setText("删除")
                    del_kernel.clicked.connect(self._delKernel)
                    self.jobInfoPage.gputable.setCellWidget(i, 5, del_kernel)
                else:
                    print("is gpu")
                    i += 1
                    item1 = QTableWidgetItem("顺序")
                    item1.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 0, item1)
                    itemx = QTableWidgetItem("硬件")
                    itemx.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 1, itemx)
                    item2 = QTableWidgetItem("线程块数")
                    item2.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 2, item2)
                    item3 = QTableWidgetItem("线程数")
                    item3.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 3, item3)
                    item4 = QTableWidgetItem("TFLOPs")
                    item4.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 4, item4)
                    item5 = QTableWidgetItem("需求显存(MB)")    
                    item5.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 5, item5)
                    item6 = QTableWidgetItem("输入(MB)")
                    item6.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 6, item6)
                    item7 = QTableWidgetItem("输出(MB)")
                    item7.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 7, item7)
                    item8 = QTableWidgetItem("类型")
                    item8.setBackground(QColor(192, 192, 192))
                    self.jobInfoPage.gputable.setItem(i, 8, item8)
                    i += 1
                    self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(int((i+1)/2))))
                    self.jobInfoPage.gputable.setItem(i, 1, QTableWidgetItem(str(kernel_info.hardware)))
                    self.jobInfoPage.gputable.setItem(i, 2, QTableWidgetItem(str(kernel_info.block_num)))
                    self.jobInfoPage.gputable.setItem(i, 3, QTableWidgetItem(str(kernel_info.thread_num)))
                    self.jobInfoPage.gputable.setItem(i, 4, QTableWidgetItem(str(kernel_info.thread_length)))
                    self.jobInfoPage.gputable.setItem(i, 5, QTableWidgetItem(str(kernel_info.requested_gddram_size)))
                    self.jobInfoPage.gputable.setItem(i, 6, QTableWidgetItem(str(kernel_info.task_input_size)))
                    self.jobInfoPage.gputable.setItem(i, 7, QTableWidgetItem(str(kernel_info.task_output_size)))
                    typeChose = QComboBox()
                    typeChose.addItem("整数")
                    typeChose.addItem("浮点")
                    typeChose.addItem("矩阵")
                    typeChose.setCurrentText(kernel_info.type)
                    self.jobInfoPage.gputable.setCellWidget(i, 8, typeChose)
                    del_kernel = QPushButton()
                    del_kernel.setText("删除")
                    del_kernel.clicked.connect(self._delKernel)
                    self.jobInfoPage.gputable.setCellWidget(i, 9, del_kernel)

        

    def _delKernel(self):
        print("del kernel")
        row = self.jobInfoPage.gputable.currentRow()
        self.jobInfoPage.gputable.removeRow(row)
        row -= 1
        self.jobInfoPage.gputable.removeRow(row)
        self.kernel_num -= 1
        for i in range(row, 2*(self.kernel_num + 1)):
            if i % 2 == 1:
                self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(int((i+1)/2))))

    def _addKernel(self):
        if self.nowJob is None:
            return
        self.kernel_num += 1
        print("add kernel: " + str(self.kernel_num))
        self.jobInfoPage.gputable.setRowCount(2*(1+self.kernel_num))
        i = 2+ 2*(self.kernel_num-1)
        self.jobInfoPage.gputable.setColumnCount(10)
        item1 = QTableWidgetItem("顺序")
        item1.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 0, item1)
        item1 = QTableWidgetItem("硬件")
        item1.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 1, item1)
        item2 = QTableWidgetItem("线程块数")
        item2.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 2, item2)
        item3 = QTableWidgetItem("线程数")
        item3.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 3, item3)
        item4 = QTableWidgetItem("TFLOPs")
        item4.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 4, item4)
        item5 = QTableWidgetItem("需求显存(MB)")    
        item5.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 5, item5)
        item6 = QTableWidgetItem("输入(MB)")
        item6.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 6, item6)
        item7 = QTableWidgetItem("输出(MB)")
        item7.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 7, item7)
        item8 = QTableWidgetItem("类型")
        item8.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 8, item8)
            
        i += 1
        self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(int((i+1)/2))))
        self.jobInfoPage.gputable.setItem(i, 1, QTableWidgetItem("GPU"))
        self.jobInfoPage.gputable.setItem(i, 2, QTableWidgetItem("10"))
        self.jobInfoPage.gputable.setItem(i, 3, QTableWidgetItem("10"))
        self.jobInfoPage.gputable.setItem(i, 4, QTableWidgetItem("100"))
        self.jobInfoPage.gputable.setItem(i, 5, QTableWidgetItem("100"))
        self.jobInfoPage.gputable.setItem(i, 6, QTableWidgetItem("100"))
        self.jobInfoPage.gputable.setItem(i, 7, QTableWidgetItem("100"))
        typeChose = QComboBox()
        typeChose.addItem("整数")
        typeChose.addItem("浮点")
        typeChose.addItem("矩阵")
        typeChose.setCurrentText("浮点")
        self.jobInfoPage.gputable.setCellWidget(i, 8, typeChose)
        del_kernel = QPushButton()
        del_kernel.setText("删除")
        del_kernel.clicked.connect(self._delKernel)
        self.jobInfoPage.gputable.setCellWidget(i, 9, del_kernel)

    def _addCpuKernel(self):
        if self.nowJob is None:
            return
        self.kernel_num += 1
        print("add kernel: " + str(self.kernel_num))
        self.jobInfoPage.gputable.setRowCount(2*(1+self.kernel_num))
        i = 2+ 2*(self.kernel_num-1)
        self.jobInfoPage.gputable.setColumnCount(9)
        item1 = QTableWidgetItem("顺序")
        item1.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 0, item1)
        item1 = QTableWidgetItem("硬件")
        item1.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 1, item1)
        item3 = QTableWidgetItem("线程数")
        item3.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 2, item3)
        item4 = QTableWidgetItem("GFLOPs")
        item4.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 3, item4)
        item5 = QTableWidgetItem("类型")
        item5.setBackground(QColor(192, 192, 192))
        self.jobInfoPage.gputable.setItem(i, 4, item5)
        i += 1
        self.jobInfoPage.gputable.setItem(i, 0, QTableWidgetItem(str(int((i+1)/2))))
        self.jobInfoPage.gputable.setItem(i, 1, QTableWidgetItem("CPU"))
        self.jobInfoPage.gputable.setItem(i, 2, QTableWidgetItem("1"))
        self.jobInfoPage.gputable.setItem(i, 3, QTableWidgetItem("10"))
        combox = QComboBox()
        combox.addItem("整数")
        combox.addItem("浮点")
        combox.addItem("矩阵")
        combox.setCurrentText("浮点")
        self.jobInfoPage.gputable.setCellWidget(i, 4, combox)
        del_kernel = QPushButton()
        del_kernel.setText("删除")
        del_kernel.clicked.connect(self._delKernel)
        self.jobInfoPage.gputable.setCellWidget(i, 5, del_kernel)

    def _applyJob(self):
        print("apply job")
        if self.nowJob is None:
            return
        if self.jobInfoPage.jobName.text().startswith("系统管理软件"):
            QMessageBox.information(self, "错误", "任务名不合法")
            self.__initJobInfo(self.nowJob)
            return
        if self.jobInfoPage.jobName.text() == "":
            QMessageBox.information(self, "错误", "任务名不能为空")
            self.__initJobInfo(self.nowJob)
            return
        if self.jobInfoPage.jobName.text() in sysSim.jobs and self.jobInfoPage.jobName.text() != self.nowJob.name:
            QMessageBox.information(self, "错误", "任务名重复")
            self.__initJobInfo(self.nowJob)
            return
        if self.jobInfoPage.ram.text() == "" or int(self.jobInfoPage.ram.text()) == 0:
            QMessageBox.information(self, "错误", "任务请求内存不能为0")
            self.__initJobInfo(self.nowJob)
            return
        if self.jobInfoPage.period.text() == "":
            QMessageBox.information(self, "错误", "任务周期不能为空")
            self.__initJobInfo(self.nowJob)
            return
        name_before = self.nowJob.name
        self.nowJob.name = self.jobInfoPage.jobName.text()
        self.nowJob.cpu_task.ram = self.jobInfoPage.ram.text()
        self.nowJob.period = self.jobInfoPage.period.text()
        # self.nowJob.cpu_task.pes_number = self.jobInfoPage.corenum.value()
        # self.nowJob.cpu_task.length = self.jobInfoPage.cpuflops.text()
        # self.nowJob.gpu_task = None
        # print(self.jobInfoPage.host.currentText())
        if self.jobInfoPage.host.currentText() != "不指定":
            self.nowJob.host = self.jobInfoPage.host.currentText()
        else:
            self.nowJob.host = ""
        request_gddram_total = 0
        task_input_size_total = 0
        task_output_size_total = 0
        kernels = []
        for i in range(self.jobInfoPage.gputable.rowCount()):
            if i%2 == 0:
                continue
            n = (i + 1) / 2
            n = n.__str__()
            if self.jobInfoPage.gputable.item(i, 1).text() == "CPU":
                if int(self.jobInfoPage.gputable.item(i, 2).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个内核的线程数不能为0")
                    continue
                if int(self.jobInfoPage.gputable.item(i, 3).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个内核的计算量不能为0")
                    continue
                combox = self.jobInfoPage.gputable.cellWidget(i, 4)
                cpuTask = GPUTaskInfo.Kernel(0, int(self.jobInfoPage.gputable.item(i, 2).text()), int(self.jobInfoPage.gputable.item(i, 3).text()), 0, 0, 0, 'CPU', combox.currentText())
                kernels.append(cpuTask)
                continue
            else:
                if int(self.jobInfoPage.gputable.item(i, 2).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个内核的线程块数不能为0")
                    continue
                if int(self.jobInfoPage.gputable.item(i, 3).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个内核的每线程块线程数不能为0")
                    continue
                if int(self.jobInfoPage.gputable.item(i, 4).text()) == 0:
                    QMessageBox.information(self, "错误", "第" + n + "个内核的每线程FLOPS不能为0")
                    continue
                combox = self.jobInfoPage.gputable.cellWidget(i, 8)
                # request_gddram_total += int(self.jobInfoPage.gputable.item(i + 1, 4).text())
                # task_input_size_total += int(self.jobInfoPage.gputable.item(i + 1, 5).text())
                # task_output_size_total += int(self.jobInfoPage.gputable.item(i + 1, 6).text())
                kernel = GPUTaskInfo.Kernel(int(self.jobInfoPage.gputable.item(i, 2).text()), int(self.jobInfoPage.gputable.item(i, 3).text()), int(self.jobInfoPage.gputable.item(i, 4).text()), int(self.jobInfoPage.gputable.item(i, 5).text()), int(self.jobInfoPage.gputable.item(i, 6).text()), int(self.jobInfoPage.gputable.item(i, 7).text()), 'GPU', combox.currentText())
                kernels.append(kernel)
        self.nowJob.gpu_task = GPUTaskInfo(kernels, request_gddram_total, task_input_size_total, task_output_size_total)
        self.__initJobInfo(self.nowJob)
        sysSim.jobs.pop(name_before)
        sysSim.jobs[self.nowJob.name] = self.nowJob
        self.nowJob.print()
        self.parent.update_tree_view()

    def _initFaultInfo(self, fault: FaultGenerator, ifTrueFault=True):
        self.showFaultInject.setChart(QChart())
        self.showFaultInject2.setChart(QChart())
        self.faultRecordTable.setRowCount(0)
        if ifTrueFault:
            print(fault.mttf_type + " 是这个")
            self.nowFault = fault
            self.faultInfoPage.aim.clear()
            self.faultInfoPage.aim.addItem(fault.aim)
            self.faultInfoPage.name.setText(fault.name)
            self.faultInfoPage.aim.setCurrentText(fault.aim)
            self.faultInfoPage.type.setCurrentText(tranFromE2C(fault.mttf_type))
            print(tranFromE2C(fault.mttf_type))
            self.faultInfoPage.time1.setText(str((int)(fault.mttf_scale)))
            regular_ex = QRegularExpression("[0-9]+")
            validator = QRegularExpressionValidator(regular_ex, self.faultInfoPage.time1)
            self.faultInfoPage.time1.setValidator(validator)
            self.faultInfoPage.time2.setText(str((int)(fault.mttr_scale)))
            regular_ex = QRegularExpression("[0-9]+")
            validator = QRegularExpressionValidator(regular_ex, self.faultInfoPage.time2)
            self.faultInfoPage.time2.setValidator(validator)
            if fault.mttf_type == "Normal":
                self.showFaultInject.setChart(self.__getNormalLine(fault.mttf_scale))
                self.showFaultInject2.setChart(self.__getNormalLine(fault.mttr_scale))
            elif fault.mttf_type == "LogNormal":
                self.showFaultInject.setChart(self.__getLogNormalLine(fault.mttf_scale))
                self.showFaultInject2.setChart(self.__getLogNormalLine(fault.mttr_scale))
            elif fault.mttf_type == "Weibull":
                self.showFaultInject.setChart(self.__getWeiBullLine(fault.mttf_scale))
                self.showFaultInject2.setChart(self.__getWeiBullLine(fault.mttr_scale))
            elif fault.mttf_type == "Gamma":
                self.showFaultInject.setChart(self.__getGammaLine(fault.mttf_scale))
                self.showFaultInject2.setChart(self.__getGammaLine(fault.mttr_scale))
            if fault.type == "CPU":
                self.faultInfoPage.hardware.setCurrentIndex(0)
            elif fault.type == "ram":
                self.faultInfoPage.hardware.setCurrentIndex(1)
             # 填充故障信息表格
            path = sysSim.path + "/OutputFiles/faultRecords.xml"
            print(path)
            if os.path.exists(path) and os.path.isdir(sysSim.path + "/OutputFiles") and os.path.isfile(sysSim.path + "/OutputFiles/faultRecords.xml"):
                print("exist")
                xmlParser = XmlParser(path)
                fault_results = xmlParser.parseFaultRecord()
                fault_num = len(fault_results)
                # 设置不可见
                self.faultRecordTable.verticalHeader().setVisible(False)
                self.faultRecordTable.horizontalHeader().setVisible(True)
                self.faultRecordTable.setColumnCount(5)
                self.faultRecordTable.setRowCount(fault_num)
                self.faultRecordTable.setHorizontalHeaderLabels(["时间", "故障对象", "类型", "恢复", "虚警"])
                i = 0
                for faultRecord in fault_results:
                    self.faultRecordTable.setItem(i, 0, QTableWidgetItem(faultRecord.time))
                    self.faultRecordTable.setItem(i, 1, QTableWidgetItem(faultRecord.object))
                    self.faultRecordTable.setItem(i, 2, QTableWidgetItem(faultRecord.type))
                    if(faultRecord.isSuccessRebuild == "True"):
                        self.faultRecordTable.setItem(i, 3, QTableWidgetItem("成功"))
                    else:
                        self.faultRecordTable.setItem(i, 3, QTableWidgetItem("失败"))
                    if(faultRecord.isFalseAlarm == "True"):
                        self.faultRecordTable.setItem(i, 4, QTableWidgetItem("是"))
                    else:
                        self.faultRecordTable.setItem(i, 4, QTableWidgetItem("否"))
                    i += 1
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
          
            #self.faultInfoPage.show.setChart(QChart())

    def _applyFault(self):
        print("apply fault")
        if self.nowFault is None:
            return
        if self.faultInfoPage.name.text() == "":
            QMessageBox.information(self, "错误", "错误模型名不能为空")
            self._initFaultInfo(self.nowFault)
            return
        if self.faultInfoPage.name.text() in sysSim.faults and self.faultInfoPage.name.text() != self.nowFault.name:
            QMessageBox.information(self, "错误", "错误模型名重复")
            self._initFaultInfo(self.nowFault)
            return
        if self.faultInfoPage.time1.text() == "":
            QMessageBox.information(self, "错误", "平均无故障时间不能为空")
            self._initFaultInfo(self.nowFault)
            return
        if self.faultInfoPage.time2.text() == "":
            QMessageBox.information(self, "错误", "平均故障修复时间不能为空")
            self._initFaultInfo(self.nowFault)
            return
        if (int)(self.faultInfoPage.time1.text()) == 0:
            QMessageBox.information(self, "错误", "平均无故障时间不能为0")
            self._initFaultInfo(self.nowFault)
            return
        if (int)(self.faultInfoPage.time2.text()) == 0:
            QMessageBox.information(self, "错误", "平均故障修复时间不能为0")
            self._initFaultInfo(self.nowFault)
            return
        name_before = self.nowFault.name
        newFault = FaultGenerator(tranFromC2E(self.faultInfoPage.type.currentText()), (float)(self.faultInfoPage.time1.text()), (float)(self.faultInfoPage.time2.text()))
        newFault.setAim(self.faultInfoPage.aim.currentText())
        newFault.setName(self.faultInfoPage.name.text())
        if self.faultInfoPage.hardware.currentText() == "CPU":
            newFault.setHardware("CPU")
        elif self.faultInfoPage.hardware.currentText() == "GPU":
            newFault.setHardware("gpu")
        else:
            newFault.setHardware("ram")
        newFault.print()
        sysSim.faults.pop(name_before)
        sysSim.faults[newFault.name] = newFault
        self.nowFault = newFault
        newFault.print()
        self._initFaultInfo(newFault)
        self.parent.update_tree_view()

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
    
    def _delJob(self):
        print("del job")
        if self.nowJob is None:
            return
        sysSim.jobs.pop(self.nowJob.name)
        self.sJMain.close()
        self.parent.update_tree_view()

    def _showInfo(self):
        print("show info")
        #获取点击item所属根节点的名称（如无根节点则返回自身）
        self.nowClect = self.parent.ui.infoList.currentItem().parent()
        if self.nowClect is None:
            return
        else:
            self.lastClect = self.nowClect.text(0)
            self.nowClect = self.nowClect.parent()
            if self.nowClect is None:
                if self.lastClect == "故障":
                    self.faultInfoPage = Ui_FaultInfo()
                    self.sF = QWidget()
                    self.faultInfoPage.setupUi(self.sF)
                    new_fault = sysSim.faults[self.parent.ui.infoList.currentItem().text(0)]
                    self.nowFault = new_fault
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
                    self._initFaultInfo(new_fault)
                    self.sF.setWindowTitle("设置故障属性")
                    self.sF.setWindowIcon(QIcon("img/仿真.png"))
                    self.sF.setGeometry(sysSim.screenSize.width() *0.3, sysSim.screenSize.height() *0.3, sysSim.screenSize.width() *0.5, sysSim.screenSize.height() *0.5)
                    self.sF.show()
                else:
                    return
            else:
                self.nowClect = self.nowClect.text(0)
                print(self.nowClect)
                if self.nowClect == "主机":
                    # 选中的是任务
                    softwareName = self.parent.ui.infoList.currentItem().text(0)
                    if softwareName == "系统管理软件":
                        return
                    if softwareName == "系统管理软件(主)":
                        os.popen(f"{globaldata.targetPath[3]} {sysSim.path} 1")
                        return
                    self.sJMain = QWidget()
                    self.sJMain.setWindowTitle("设置软件属性")
                    self.sJMain.setWindowIcon(QIcon("img/仿真.png"))
                    hL = QHBoxLayout()
                    self.sJMain.setLayout(hL)
                    self.sJTab = QTabWidget(self.sJMain)
                    hL.addWidget(self.sJTab)
                    self.sJ = QWidget()
                    self.jobInfoPage = Ui_JobInfo()
                    self.jobInfoPage.setupUi(self.sJ)
                    self.sJTab.addTab(self.sJ, "计算信息")
                    self.hostApp = HostNetargsAppEditorApp("", True)
                    self.sJTab.addTab(self.hostApp, "网络流")
                    self.hostMiddleware = HostNetargsAppEditorMiddleware("", True)
                    self.sJTab.addTab(self.hostMiddleware, "网络中间件")
                    new_job = sysSim.jobs[self.parent.ui.infoList.currentItem().text(0)]
                    self.nowJob = new_job
                    self.jobInfoPage.pushButton.setIcon(QIcon("img/加.png"))
                    self.jobInfoPage.apply.clicked.connect(self._applyJob)
                    self.jobInfoPage.delete_2.clicked.connect(self._delJob)
                    self.addJobMenu = QMenu(self)
                    self.cpuAc = QAction("CPU运行")
                    self.gpuAc = QAction("GPU运行")
                    #self.cpuAc.triggered.connect(self._cpuRun)
                    self.gpuAc.triggered.connect(self._addKernel)
                    self.cpuAc.triggered.connect(self._addCpuKernel)
                    self.addJobMenu.addAction(self.cpuAc)
                    self.addJobMenu.addAction(self.gpuAc)
                    self.jobInfoPage.pushButton.setMenu(self.addJobMenu)
                    self.__initJobInfo(new_job)
                    self.sJMain.setGeometry(sysSim.screenSize.width() *0.3, sysSim.screenSize.height() *0.3, sysSim.screenSize.width() *0.5, sysSim.screenSize.height() *0.5)
                    self.sJMain.show()
        