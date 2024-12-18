from qdarktheme.qtpy.QtWidgets import (
    QWidget,
    QGraphicsView,
    QMenu,
    QGraphicsPathItem,
    QGraphicsItemGroup,
    QGraphicsSceneMouseEvent,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QTreeWidget,
    QTreeWidgetItem,
    QPushButton,
    QTabWidget,
)
from functools import partial
from PySide6.QtCharts import QChartView, QChart
import time
import os
from scene import GraphicScene
from item import GraphicItem, HostGraphicItem, SwitchGraphicItem
from MasterScene import MasterGraphicItem
from util.jobSim import sysSim
from qdarktheme.qtpy.QtCore import Qt, QRect, QRegularExpression
from qdarktheme.qtpy.QtGui import QPainter, QAction, QCursor, QIcon, QFont, QColor, QRegularExpressionValidator
from component.util import Ui_Util
from util.jobSim import sysSim
from jobSimPainter import XmlParser, Painter, Topo, TopoHost, Topos
from MasterScene import MasterScene

class MasterView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.time = 0
        self.menu = QMenu(self)
        self.seeCPU = QAction("查看CPU", self)
        self.seeCPU.triggered.connect(self.seeCPUMore)
        self.seeMemory = QAction("查看内存", self)
        self.seeMemory.triggered.connect(self.seeMemoryMore)
        self.seeGPU = QAction("查看GPU", self)
        self.seeGPU.triggered.connect(self.seeGPUMore)
        self._initOutputFiles()

    def setTreeWidget(self, treeWidget):
        self.treeWidget = treeWidget

    def setRebuildRecordTable(self, rebuildRecordTable):
        self.faultTable = rebuildRecordTable

    def connectRunButton(self, button):
        self.runButton = button
        #self.runButton.clicked.connect(self.startRun)

    def _initOutputFiles(self):
        if not os.path.isdir(sysSim.path + "/OutputFiles"):
            os.mkdir(sysSim.path + "/OutputFiles")
        if not os.path.exists(sysSim.path + "/OutputFiles/hostUtils.xml"):
            with open(sysSim.path + "/OutputFiles/hostUtils.xml", "w") as f:
                f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
                f.write("<hostUtilization>")
                f.write("</hostUtilization>")
        if not os.path.exists(sysSim.path + "/OutputFiles/jobRun.xml"):
            with open(sysSim.path + "/OutputFiles/jobRun.xml", "w") as f:
                f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
                f.write("<jobRun>")
                f.write("</jobRun>")
        if not os.path.exists(sysSim.path + "/OutputFiles/faultRecords.xml"):
            with open(sysSim.path + "/OutputFiles/faultRecords.xml", "w") as f:
                f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
                f.write("<faultRecord>")
                f.write("  <reliability value=\"1\" />")
                f.write("</faultRecord>")
        if not os.path.exists(sysSim.path + "/OutputFiles/hostFail.xml"):
            with open(sysSim.path + "/OutputFiles/hostFail.xml", "w") as f:
                f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
                f.write("<jobRun>")
                f.write("<Run time=\"100\">")
                f.write("</jobRun>")
        

    def parseOutputFiles(self):
        path = sysSim.path + "/OutputFiles/hostUtils.xml"
        print("解析以下文件：" + path)
        xmlParser = XmlParser(path)
        self.cluster_result = xmlParser.parseHostRecord()
        path = sysSim.path + "/OutputFiles/jobRun.xml"
        print("解析以下文件：" + path)
        xmlParser = XmlParser(path)
        self.job_results = xmlParser.parseJobRecord()
        path = sysSim.path + "/OutputFiles/faultRecords.xml"
        print("解析以下文件：" + path)
        xmlParser = XmlParser(path)
        self.fault_results = xmlParser.parseFaultRecord()
        self.reliable = xmlParser.parseReliabilityRecord()
        path = sysSim.path + "/OutputFiles/topoChange.xml"
        print("解析以下文件：" + path)
        xmlParser = XmlParser(path)
        self.topo_results = xmlParser.parseTopo()
        self.nowTopo = self.topo_results.topos[0]
        self.job2host = {}
        for host in self.nowTopo.hosts:
            for software in host.softwares:
                self.job2host[software] = host.name
        self.getTreeWidget().clear()
        self.getTreeWidget().setHeaderLabel("节点")
        
        itemHost = QTreeWidgetItem(self.getTreeWidget(), ["主机"])
        for hostName in sysSim.hosts:
            host = sysSim.hosts[hostName]
            item = QTreeWidgetItem(itemHost, [hostName])
            item.addChild(QTreeWidgetItem([sysSim.manager[hostName].name]))
            for name in sysSim.jobs:
                job = sysSim.jobs[name]
                if job.host == hostName:
                    item.addChild(QTreeWidgetItem([job.name]))
            itemHost.addChild(item)

        self.getTreeWidget().expandAll()

        fault_num = 0
        for faultRecord in self.fault_results:
            if faultRecord.type == "主机宕机":
                fault_num += 1
        self.faultTable.verticalHeader().setVisible(False)
        self.faultTable.horizontalHeader().setVisible(True)
        self.faultTable.setColumnCount(4)
        self.faultTable.setRowCount(fault_num)
        self.faultTable.setHorizontalHeaderLabels(["时间", "故障对象", "故障硬件","查看重构"])
        i = 0
        num = 0
        for faultRecord in self.fault_results:
            if faultRecord.type != "主机宕机":
                continue
            seeMore = QPushButton()
            seeMore.setText("查看")
            if faultRecord.ifEmpty == "False":
                num += 1
                seeMore.clicked.connect(partial(self.paintFrame, self.topo_results.topos[num], self.topo_results.topos[num - 1]))
            else:
                seeMore.clicked.connect(partial(self.paintFrame, self.topo_results.topos[num], self.topo_results.topos[num]))
            self.faultTable.setItem(i, 0, QTableWidgetItem(faultRecord.time))
            self.faultTable.setItem(i, 1, QTableWidgetItem(faultRecord.object))
            if faultRecord.hardware == "CPU" or faultRecord.hardware == "cpu":
                self.faultTable.setItem(i, 2, QTableWidgetItem("CPU"))
            elif faultRecord.hardware == "ram" or faultRecord.hardware == "RAM" or faultRecord.hardware == "内存":
                self.faultTable.setItem(i, 2, QTableWidgetItem("内存"))
            elif faultRecord.hardware == "GPU" or faultRecord.hardware == "gpu":
                self.faultTable.setItem(i, 2, QTableWidgetItem("GPU"))
            else:
                self.faultTable.setItem(i, 2, QTableWidgetItem("\\"))
            self.faultTable.setCellWidget(i, 3, seeMore)
            i += 1

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
        self.jobTabWidget.addTab(self.jobTable, "任务运行情况")

        self.jobRunTable = QTableWidget()
        # 设置不可见
        self.jobRunTable.verticalHeader().setVisible(False)
        self.jobRunTable.horizontalHeader().setVisible(True)
        self.jobRunTable.setColumnCount(5)
        self.jobRunTable.setRowCount(0)
        self.jobRunTable.setHorizontalHeaderLabels(["任务名", "主机", "开始", "结束","状态"])
        self.jobTabWidget.addTab(self.jobRunTable, "任务运行记录")

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

        self.jobTabWidget.setCurrentIndex(1)
        

    def setJobTab(self, jobTabWidget: QTabWidget):
        self.jobTabWidget = jobTabWidget

    def paintFrame(self, topo: Topo, last: Topo):
        self.changeSofwares = []
        for host in last.hosts:
            for software in host.softwares:
                self.job2host[software] = host.name
        for host in topo.hosts:
            for software in host.softwares:
                if software not in self.job2host:
                    #self.changeSofwares.append([software, "null", host.name])
                    self.job2host[software] = host.name
                if self.job2host[software] != host.name:
                    self.changeSofwares.append([software, self.job2host[software], host.name])
                    self.job2host[software] = host.name
    
        self.getTreeWidget().clear()
        self.getTreeWidget().setHeaderLabel("节点")
        
        itemHost = QTreeWidgetItem(self.getTreeWidget(), ["主机"])
        for host in topo.hosts:
            item = QTreeWidgetItem(itemHost, [host.name])
            print("add host " + host.name)
            item.addChild(QTreeWidgetItem([sysSim.manager[host.name].name]))
            for software in host.softwares:
                item.addChild(QTreeWidgetItem([software]))
                print("software " + software)
            itemHost.addChild(item)

        self.getTreeWidget().expandAll()

        scene = MasterScene(self.runButton, self)
        scene.printNet(self.changeSofwares)
        self.setScene(scene)
        

    def startRun(self):
        self.runButton.setEnabled(False)
        for topo in self.topo_results.topos:
            self.paintFrame(topo)
            time.sleep(1)
        self.runButton.setEnabled(True)

        

    def setScene(self, scene: MasterScene):
        self.mscene = scene
        return super().setScene(scene)

    def graphicItemClicked(self, item, event: QGraphicsSceneMouseEvent):
        print("item clicked")
        self.item_clicked = item
        self.menu = QMenu(self)
        if isinstance(self.item_clicked, MasterGraphicItem):
            print("MasterGraphicItem")
            name = item.name
            host = sysSim.hosts[name]
            self.menu.addAction(self.seeCPU)
            self.menu.addAction(self.seeMemory)
            if len(host.video_card_infos) > 0:
                self.menu.addAction(self.seeGPU)
            self.menu.popup(QCursor.pos())
        if event.button() == Qt.MouseButton.RightButton:
            print("右键")
            print(item.name)
            self.menu.popup(QCursor.pos())

    def getTreeWidget(self) -> QTreeWidget:
        return self.treeWidget
    
    def getRebuildRecordTable(self) -> QTableWidget:
        return self.faultTable
    
    def seeCPUMore(self):
        self.cpuMore = QWidget()
        self.cpuMoreUI = Ui_Util()
        self.cpuMoreUI.setupUi(self.cpuMore)
        self.cpuMore.setWindowTitle("CPU信息")
        self.cpuMore.setWindowIcon(QIcon("img/仿真.png"))
        painter = Painter(self.cluster_result, [], [])
        chartCPU = painter.plotHostCPUUtilization(self.item_clicked.name, -1, float("inf"))
        self.cpuLine = QChartView(self.cpuMore)
        self.cpuLine.setChart(chartCPU)
        self.cpuLine.setRenderHint(QPainter.Antialiasing)
        self.cpuMoreUI.tabWidget.addTab(self.cpuLine, "利用率曲线")
        self.cpuTable = painter.tableHostCPUUtilization(self.item_clicked.name, -1, float("inf"))
        self.cpuMoreUI.hostMore.setRowCount(len(self.cpuTable))
        self.cpuMoreUI.hostMore.setColumnCount(2)
        self.cpuMoreUI.hostMore.verticalHeader().setVisible(False)
        self.cpuMoreUI.hostMore.horizontalHeader().setVisible(True)
        self.cpuMoreUI.hostMore.setHorizontalHeaderLabels(["时间", "利用率"])
        for i in range(len(self.cpuTable)):
            self.cpuMoreUI.hostMore.setItem(i, 0, QTableWidgetItem(str(self.cpuTable[i][0])))
            self.cpuMoreUI.hostMore.setItem(i, 1, QTableWidgetItem(str(self.cpuTable[i][1])))
        self.cpuMore.show()

    def seeMemoryMore(self):
        self.memoryMore = QWidget()
        self.memoryMoreUI = Ui_Util()
        self.memoryMoreUI.setupUi(self.memoryMore)
        self.memoryMore.setWindowTitle("内存信息")
        self.memoryMore.setWindowIcon(QIcon("img/仿真.png"))
        painter = Painter(self.cluster_result, [], [])
        chartRAM = painter.plotHostRamUtilization(self.item_clicked.name, -1, float("inf"))
        self.ramLine = QChartView(self.memoryMore)
        self.ramLine.setChart(chartRAM)
        self.ramLine.setRenderHint(QPainter.Antialiasing)
        self.memoryMoreUI.tabWidget.addTab(self.ramLine, "利用率曲线")
        self.memoryTable = painter.tableHostRamUtilization(self.item_clicked.name, -1, float("inf"))
        self.memoryMoreUI.hostMore.setRowCount(len(self.memoryTable))
        self.memoryMoreUI.hostMore.setColumnCount(2)
        self.memoryMoreUI.hostMore.verticalHeader().setVisible(False)
        self.memoryMoreUI.hostMore.horizontalHeader().setVisible(True)
        self.memoryMoreUI.hostMore.setHorizontalHeaderLabels(["时间", "利用率"])
        for i in range(len(self.memoryTable)):
            self.memoryMoreUI.hostMore.setItem(i, 0, QTableWidgetItem(str(self.memoryTable[i][0])))
            self.memoryMoreUI.hostMore.setItem(i, 1, QTableWidgetItem(str(self.memoryTable[i][1])))
        self.memoryMore.show()

    def seeGPUMore(self):
        self.gpuMore = QWidget()
        self.gpuMoreUI = Ui_Util()
        self.gpuMoreUI.setupUi(self.gpuMore)
        self.gpuMore.setWindowTitle("GPU信息")
        self.gpuMore.setWindowIcon(QIcon("img/仿真.png"))
        painter = Painter(self.cluster_result, [], [])
        chartGPU = painter.plotGpuUtilization(self.item_clicked.name, -1, float("inf"))
        self.gpuLine = QChartView(self.gpuMore)
        self.gpuLine.setChart(chartGPU)
        self.gpuLine.setRenderHint(QPainter.Antialiasing)
        self.gpuMoreUI.tabWidget.addTab(self.gpuLine, "利用率曲线")
        self.gpuTable = painter.tableGpuUtilization(self.item_clicked.name, -1, float("inf"))
        if len(self.gpuTable) == 0:
            return
        self.gpuMoreUI.hostMore.setRowCount(len(self.gpuTable[0]))
        self.gpuMoreUI.hostMore.setColumnCount(len(self.gpuTable) + 1)
        self.gpuMoreUI.hostMore.verticalHeader().setVisible(False)
        self.gpuMoreUI.hostMore.horizontalHeader().setVisible(True)
        self.gpuMoreUI.hostMore.setHorizontalHeaderLabels(["时间"] + ["利用率 " + str(i) for i in range(len(self.gpuTable))])
        for i in range(len(self.gpuTable[0])):
            self.gpuMoreUI.hostMore.setItem(i, 0, QTableWidgetItem(str(self.gpuTable[0][i][0])))
            for j in range(len(self.gpuTable)):
                self.gpuMoreUI.hostMore.setItem(i, j + 1, QTableWidgetItem(str(self.gpuTable[j][i][1])))
        self.gpuMore.show()

        

    
