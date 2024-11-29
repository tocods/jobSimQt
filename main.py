# ---------------------------------------------------------------------------------------------
#  Copyright (c) Yunosuke Ohsugi. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------*/

import sys
import json
import webbrowser
import subprocess
import os
import numpy as np
from scipy import stats
import random
from functools import partial
import project
import qdarktheme
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot, QRegularExpression, QUrl, QRectF
from qdarktheme.qtpy.QtGui import *
from qdarktheme.qtpy.QtWidgets import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtNetwork import QNetworkCookie
from main_ui import UI
from util.jobSim import sysSim, ParseUtil, HostInfo, CPUInfo, GPUInfo, VideoCardInfo, JobInfo, CPUTaskInfo, GPUTaskInfo, FaultGenerator, tranFromC2E, tranFromE2C, LinkNet, HostNet, SwtichNet, FlowNet
from jobSimPage import JobSimPage
from component.hostinfo import Ui_HostInfo
from component.jobinfo import Ui_JobInfo
from component.faultinfo import Ui_FaultInfo
from PySide6.QtCharts import QChart,QChartView,QLineSeries,QDateTimeAxis,QValueAxis, QPieSeries, QScatterSeries, QBarSeries, QBarSet
from jobSimPainter import Painter, XmlParser
from util.table import NumericDelegate
from resultUtil import getAverageRunTime, getAverageRunTimeInHost, getThroughput, getEfficiency
import globaldata
from item import GraphicItem
from edge import Edge
import xml.etree.ElementTree as ET
from xml.dom import minidom
from ShowNetResultsWindow import ShowNetResultsWindow


class NetResultType:
    def __init__(self):
        self.type = ""
        self.backlog_bound = 0
        self.delay_bound = 0

class NetResult:
    def __init__(self):
        self.nresults = []

    def addResultType(self, r):
        self.nresults.append(r)

    

class JobSimQt(QMainWindow):
    def __init__(self, path, tab) -> None:
        super().__init__()
        self.duration = 100
        print(path)
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        project.projectPath = path
        globaldata.currentProjectInfo.setFullPath(path)
        self._initOutputFiles()
        # 保存当前文件路径
        if getattr(sys, 'frozen', False):
            self.selfPath = os.path.dirname(sys.executable)
        else:
            self.selfPath = os.path.dirname(os.path.abspath(__file__))
        self.pathTxt = self.selfPath + "/path.txt"
        if not os.path.isfile(self.pathTxt):
            QMessageBox.information(self, "提示", "请先设置仿真工具路径:" + self.pathTxt, QMessageBox.Ok)
            return
        self.netSecruityPath = ""
        self.grafanaPath = ""
        self.javaPath = ""
        with open(self.pathTxt, "r") as f:
            lines = f.readlines()
            for line in lines:
                # 移除换行符
                line = line.strip('\n')
                if line == "":
                    continue
                if line.startswith("netSecurity="):
                    self.netSecurityPath = line.split("=")[1]
                if line.startswith("grafana="):
                    self.grafanaPath = line.split("=")[1]
                if line.startswith("java="):
                    self.javaPath = line.split("=")[1]
        # 取消标题栏
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("系统管理评估平台")
        self.setWindowIcon(QIcon(self.selfPath + "/img/数据.png"))
        self.nowClect = None
        self._ui = UI()
        self._ui.setup_ui(self, self.selfPath, tab)
        self.tab = tab
        if tab == -1:
            self._ui.stack_widget.addWidget(self._ui.stack_1)
            self._ui.stack_widget.addWidget(self._ui.stack_2)
            self._ui.stack_widget.addWidget(self._ui.stack_3)
        if tab == 0:
            self._ui.stack_widget.addWidget(self._ui.stack_1)
        if tab == 1:
            self._ui.stack_widget.addWidget(self._ui.stack_2)
        self._ui.stack_widget.setCurrentIndex(0)
        # Signal
        if tab == -1:
            self._ui.action_change_home.triggered.connect(self._change_page)
            self._ui.action_change_dock.triggered.connect(self._change_page)
            self._ui.action_micro_service.triggered.connect(self._change_page)
            self._ui.action_net_safe.triggered.connect(self._change_page)
        if tab == 0:
            self._ui.action_change_home.triggered.connect(self._change_page)
        if tab == 1:
            self._ui.action_change_dock.triggered.connect(self._change_page)
        self._ui.action_refresh.triggered.connect(self._initAll)
        self._ui.action_open_folder.triggered.connect(self.loadFromProject
            #lambda: QFileDialog.getOpenFileName(self, "Open File", options=QFileDialog.Option.DontUseNativeDialog)
        )
        self._ui.action_out.triggered.connect(sys.exit)
        # self._ui.action_enable.triggered.connect(self._toggle_state)
        # self._ui.action_disable.triggered.connect(self._toggle_state)
        for action in self._ui.actions_theme:
            action.triggered.connect(self._change_theme)
        self._ui.stack_1.netCalUi.chose.clicked.connect(self.__choseFlow)
        self._ui.stack_1.netCalUi.run.clicked.connect(self.__runNetAnalysis)
        screen = QGuiApplication.screens()[0]
        screen_size = screen.availableGeometry()
        self.setGeometry(0, 0, screen_size.width() * 0.9, screen_size.height() * 0.9)
        #self._ui.resultui.layoutWidget.setGeometry(0, 0, screen_size.width() * 0.8, screen_size.height() * 0.8)
        self._initAll()

    def center(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    @Slot()
    def _change_page(self) -> None:
        action_name = self.sender().text()
        if action_name == "网络仿真结果分析":
            self._ui.stack_widget.setCurrentIndex(0)
        if action_name == "系统管理仿真结果分析":
            if self.tab != 1:
                self._ui.stack_widget.setCurrentIndex(1)
            else:
                self._ui.stack_widget.setCurrentIndex(0)
        if action_name == "微服务指标采集":
                    # 初始化一个page
            if self.grafanaPath == "":
                QMessageBox.information(self, "提示", "缺少微服务指标采集页面路径", QMessageBox.Ok)
                return
            self.webview = QWebEngineView(self._ui.stack_3)
            #self.weburl="http://localhost:3000/d/IV0hu1m7z/windows-exporter-dashboard?var-interval=60s&from=now-2d&to=now&timezone=browser&var-server=localhost:9182&refresh=5s"
            webbrowser.open(self.grafanaPath)
            #self.save_cookies()
            #self.load_cookies()
            # 加载一个网页，以便产生一些 cookies
            self.webview.page().load(QUrl(self.grafanaPath))
            self.webview.show()
            #self.cookie_store.cookieAdded.connect(self.handlecookie))
            #页面加载完成执行
            #self.view.page().loadFinished.connect(self.on_page_load_finished)
            screen = QGuiApplication.screens()[0]
            screen_size = screen.availableGeometry()
            self._ui.stack_3.setGeometry(0, 0, screen_size.width() * 0.8, screen_size.height() * 0.8)
            self.webview.setGeometry(0, 0, screen_size.width() * 0.8, screen_size.height() * 0.8)
            #self._ui.stack_widget.setCurrentIndex(2)
        if action_name == "网络安全评估":
            if self.netSecurityPath == "":
                QMessageBox.information(self, "提示", "缺少网络安全评估软件可执行文件路径", QMessageBox.Ok)
                return
            subprocess.Popen(self.netSecurityPath)
    
    # def load_cookies(self):
    #     profile = self.webview.page().profile()
    #     self.cookie_store = profile.cookieStore()
    #     with open('cookies.txt', 'r') as file:
    #         for line in file:
    #             # 创建一个cookie
    #             cookie = QNetworkCookie()
    #             mycookie=cookie.parseCookies(line.encode("utf-8"))
    #             print(mycookie)
    #             # 将cookie添加到cookie存储
    #             self.cookie_store.setCookie(mycookie[0])
    #     self.cookie_store.loadAllCookies()

    @Slot()
    def _toggle_state(self) -> None:
        state = self.sender().text()
        self._ui.central_window.centralWidget().setEnabled(state == "Enable")
        self.statusBar().showMessage(state)

    @Slot()
    def _change_theme(self) -> None:
        theme = self.sender().text()
        if theme == "黑色":
            theme = "dark"
        elif theme == "白色":
            theme = "light"
        QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet(theme))

    def saveToProject(self):
       return

    def loadFromProject(self):
        file_name = QFileDialog.getExistingDirectory(None, "Open File", "")
        print(file_name)
        globaldata.currentProjectInfo.setFullPath(file_name)
        self._ui.stack_1.reload()
        project.projectPath = file_name
        globaldata.currentProjectInfo.setFullPath(file_name)
        self._initOutputFiles()
        self._ui.stack_widget.setCurrentIndex(1)
        self._ui.resultui.hostTabs.clear()
        self._ui.resultui.jobTabs.clear()
        self._ui.resultui.faultTabs.clear()
        #self._ui.resultui.show.setChart(QChart())
        self.cpushow.setChart(QChart())
        self.ramshow.setChart(QChart())
        self.gpushow.setChart(QChart())
        self.totalshow.setChart(QChart())
        # self._ui.resultui.showCPU.setChart(QChart())
        # self._ui.resultui.showRam.setChart(QChart())
        # self._ui.resultui.showGPU.setChart(QChart())
        # self._ui.resultui.faultResultAnalysis.setChart(QChart())
        # self._ui.resultui.jobResultAnalysis.setChart(QChart())
        self._ui.resultui.faultResult.clear()
        self._ui.resultui.jobshow1.clear()
        self._ui.resultui.jobshow2.clear()
        self._ui.resultui.jobShow3.clear()
        self._initAll()
        self._ui.stack_widget.setCurrentIndex(0)
        #self.setClicked()
    
    def _initOutputFiles(self):
        if not os.path.isdir(project.projectPath + "/OutputFiles"):
            os.mkdir(project.projectPath + "/OutputFiles")
        if not os.path.exists(project.projectPath + "/OutputFiles/hostUtils.xml"):
            with open(project.projectPath + "/OutputFiles/hostUtils.xml", "w") as f:
                f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
                f.write("<hostUtilization>")
                f.write("</hostUtilization>")
        if not os.path.exists(project.projectPath + "/OutputFiles/jobRun.xml"):
            with open(project.projectPath + "/OutputFiles/jobRun.xml", "w") as f:
                f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
                f.write("<jobRun>")
                f.write("</jobRun>")
        if not os.path.exists(project.projectPath + "/OutputFiles/faultRecords.xml"):
            with open(project.projectPath + "/OutputFiles/faultRecords.xml", "w") as f:
                f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
                f.write("<faultRecord>")
                f.write("  <reliability value=\"1\" />")
                f.write("</faultRecord>")
    
    def _initAll(self):
        print("init all")
        print(project.projectPath)
        sysSim.hosts = {}
        sysSim.jobs = {}
        sysSim.faults = {}
        self.chosing = False
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
        self.__initNetAnalysis()
        self._initJobResult()

        

    def __choseFlow(self):
        print("chose " + self.chosing.__str__())
        if self.chosing == False:
            self.__printNet()
            self._ui.stack_1.netCalUi.nets.setEnabled(True)
            self._ui.stack_1.netCalUi.run.setEnabled(False)
            self.chosing = True
            self._ui.stack_1.netCalUi.chose.setText("添加")
        else:
            self._ui.stack_1.netCalUi.nets.setEnabled(False)
            self._ui.stack_1.netCalUi.run.setEnabled(True)
            self.chosing = False
            self._ui.stack_1.netCalUi.chose.setText("选择流")
            row = self._ui.stack_1.netCalUi.shows.rowCount()
            self.nowFlow.name = "Flow_" + row.__str__()
            self.flows.append(self.nowFlow)
            self.nowFlow.printNodes()
            self.nowFlow = None
            self.lastChose = None
            self.lastlastChose = None
            
            self._ui.stack_1.netCalUi.shows.setRowCount(row+1)
            self._ui.stack_1.netCalUi.shows.setItem(row, 0, QTableWidgetItem("Flow_" + (row+1).__str__()))
            show = QPushButton()
            show.setText("展示")
            show.clicked.connect(self.showNetFlow)
            self._ui.stack_1.netCalUi.shows.setCellWidget(row, 1, show)
            dels = QPushButton()
            dels.setText("删除")
            dels.clicked.connect(self.delNetFlow)
            self._ui.stack_1.netCalUi.shows.setCellWidget(row, 2, dels)
            self.__printNet()
            
    def showNetFlow(self):
        self.__printNet()
        row = self._ui.stack_1.netCalUi.shows.currentRow()
        flow = self.flows[row]
        for name in flow.nodes:
            x = -1
            y = -1
            if name in self.netHosts:
                x = self.netHosts[name].x
                y = self.netHosts[name].y
            if name in self.netSwtichs:
                x = self.netSwtichs[name].x
                y = self.netSwtichs[name].y
            rect = QRectF()
            rect.setX(float(x))
            rect.setY(float(y))
            rect.setWidth(100)
            rect.setHeight(100)
            c = QColor(Qt.red)
            self.screne.addRect(rect, c)
    
    def delNetFlow(self):
        self.__printNet()
        row = self._ui.stack_1.netCalUi.shows.currentRow()
        self.flows.pop(row)
        self._ui.stack_1.netCalUi.shows.removeRow(row)

    def __runNetAnalysis(self):
        root = ET.Element("Flows")

        for flow in self.flows:
            f = ET.SubElement(root, "Flow")
            for node in flow.nodes:
                n = ET.SubElement(f, "node")
                n.set("name", node)

        xml_str = ET.tostring(root, encoding="unicode")

        parsed_xml_str = minidom.parseString(xml_str)
        formatted_xml_str = parsed_xml_str.toprettyxml(indent="    ")
        with open(project.projectPath + "/flow_data.xml", "w") as f:
            f.write(formatted_xml_str)
        if self.javaPath == "":
            QMessageBox.information(self, "提示", "缺少java路径", QMessageBox.Ok)
            return
        subprocess.run("netcal.exe " + project.projectPath + "/network_data.xml " + project.projectPath + "/flow_data.xml " + project.projectPath + "/OutputFiles")
        self.readNetResult()
        self.__printNet()

    
    def readNetResult(self):
        print("read")
        if not os.path.isdir(project.projectPath + "/OutputFiles"):
            return
        if not os.path.isfile(project.projectPath + "/OutputFiles/NetworkAnalysisResults.xml"):
            return
        print("lala")
        root = ET.parse(project.projectPath + "/OutputFiles/NetworkAnalysisResults.xml").getroot()
        self.netResults = []
        for element in root.findall("NetworkAnalysisResult"):
            result = NetResult()
            for e1 in element.findall("TotalFlowAnalysis"):
                r = NetResultType()
                r.type = "TFA"
                r.backlog_bound = round((float)(e1.attrib['backlog_bound']), 2)
                r.delay_bound = round((float)(e1.attrib['delay_bound']), 2)
                result.addResultType(r)
                break
            for e1 in element.findall("SeparatedFlowAnalysis"):
                r = NetResultType()
                r.type = "SFA"
                r.backlog_bound = round((float)(e1.attrib['backlog_bound']), 2)
                r.delay_bound = round((float)(e1.attrib['delay_bound']), 2)
                result.addResultType(r)
                break
            for e1 in element.findall("PMOOAnalysis"):
                r = NetResultType()
                r.type = "PMO"
                r.backlog_bound = round((float)(e1.attrib['backlog_bound']), 2)
                r.delay_bound = round((float)(e1.attrib['delay_bound']), 2)
                result.addResultType(r)
                break
            for e1 in element.findall("TandemMatchingAnalysis"):
                r = NetResultType()
                r.type = "TMA"
                r.backlog_bound = round((float)(e1.attrib['backlog_bound']), 2)
                r.delay_bound = round((float)(e1.attrib['delay_bound']), 2)
                result.addResultType(r)
                break
            self.netResults.append(result)
        self.netResultTable = QTableWidget()
        self.delayChart = QChartView()
        self.backChart = QChartView()
        self.netResultTable.verticalHeader().setVisible(False)
        self.netResultTable.horizontalHeader().setVisible(False)
        self.netResultTable.setColumnCount(3)
        self.netResultTable.setRowCount(len(self.netResults) + 1)
        self.netResultTable.setItem(0, 0, QTableWidgetItem("流"))
        self.netResultTable.setItem(0, 1, QTableWidgetItem("端到端总延迟"))
        self.netResultTable.setItem(0, 2, QTableWidgetItem("最大缓冲区上界"))
        i = 0
        for result in self.netResults:
            i = i + 1
            self.netResultTable.setItem(i, 0, QTableWidgetItem("Flow_" + i.__str__()))
            p = QPushButton("查看")
            p.clicked.connect(self.showDelay)
            self.netResultTable.setCellWidget(i, 1, p)
            q = QPushButton("查看")
            q.clicked.connect(self.showBack)
            self.netResultTable.setCellWidget(i, 2, q)
        self._ui.stack_1.netCalUi.results.clear()
        self._ui.stack_1.netCalUi.results.addTab(self.netResultTable, "结果")
        self._ui.stack_1.netCalUi.results.addTab(self.delayChart, "端到端总延迟")
        self._ui.stack_1.netCalUi.results.addTab(self.backChart, "最大缓冲区上界")
        
    def showDelay(self):
        bar1 = QBarSet("TFA")
        bar2 = QBarSet("SFA")
        bar3 = QBarSet("PMO")
        bar4 = QBarSet("TMA")
        index = self.netResultTable.currentRow() - 1
        result = self.netResults[index]
        bar1.append(result.nresults[0].delay_bound)
        bar2.append(result.nresults[1].delay_bound)
        bar3.append(result.nresults[2].delay_bound)
        bar4.append(result.nresults[3].delay_bound)
        ser = QBarSeries()
        ser.append(bar1)
        ser.append(bar2)
        ser.append(bar3)
        ser.append(bar4)
        chart = QChart()
        chart.addSeries(ser)
        # chart.setTitle('CPU利用率')
        chart.createDefaultAxes()
        chart.axisY().setTitleText("端到端总延迟")
        self.delayChart.setChart(chart)
        self._ui.stack_1.netCalUi.results.setCurrentIndex(1)

    def showBack(self):
        bar1 = QBarSet("TFA")
        bar2 = QBarSet("SFA")
        bar3 = QBarSet("PMO")
        bar4 = QBarSet("TMA")
        index = self.netResultTable.currentRow() - 1
        result = self.netResults[index]
        bar1.append(result.nresults[0].backlog_bound)
        bar2.append(result.nresults[1].backlog_bound)
        bar3.append(result.nresults[2].backlog_bound)
        bar4.append(result.nresults[3].backlog_bound)
        ser = QBarSeries()
        ser.append(bar1)
        ser.append(bar2)
        ser.append(bar3)
        ser.append(bar4)
        chart = QChart()
        chart.addSeries(ser)
        # chart.setTitle('CPU利用率')
        chart.createDefaultAxes()
        chart.axisY().setTitleText("最大缓冲区上界")
        self.backChart.setChart(chart)
        self._ui.stack_1.netCalUi.results.setCurrentIndex(2)

    def __initNetAnalysis(self):
        self._ui.stack_1.netCalUi.shows.setRowCount(0)
        self._ui.stack_1.netCalUi.shows.setColumnCount(4)
        self._ui.stack_1.netCalUi.shows.setHorizontalHeaderLabels(["流", "数据大小(MB)", "", ""])
        self._ui.stack_1.netCalUi.shows.verticalHeader().setVisible(False)
        self._ui.stack_1.netCalUi.shows.horizontalHeader().setVisible(True)
        self.chosing = False
        self.nowFlow = None
        self.lastChose = None
        self.lastlastChose = None
        self.flows = []
        self.netHosts = {}
        self.netSwtichs = {}
        self.netLinks = {}
        self.netHostsPic = {}
        self.netSwtichsPic = {}
        self.netLinksPic = {}
        parser = ParseUtil()
        path = project.projectPath + "/network_data.xml"
        hosts = parser.parse_nethost_xml(path)
        switches = parser.parse_netswtich_xml(path)
        links = parser.parse_netlink_xml(path)
        for host in hosts:
            self.netHosts[host.name] = host
        for switch in switches:
            self.netSwtichs[switch.name] = switch
        for link in links:
            self.netLinks[link.name] = link
        self.__printNet()
     
    def __printNet(self):
        self.screne = QGraphicsScene()
        for host in self.netHosts.values():
            p = GraphicItem(self.selfPath + "/" + host.image, host.name, self)
            self.netHostsPic[host.name] = p
            self.screne.addItem(p)
            p.setPos(float(host.x), float(host.y))
        for switch in self.netSwtichs.values():
            p = GraphicItem(self.selfPath + "/" + switch.image, switch.name, self)
            self.netSwtichsPic[switch.name] = p
            self.screne.addItem(p)
            p.setPos(float(switch.x), float(switch.y))
        for link in self.netLinks.values():
            e1 = None
            e2 = None
            if link.p1 in self.netHostsPic:
                e1 = self.netHostsPic[link.p1]
            elif link.p1 in self.netSwtichsPic:
                e2 = self.netSwtichsPic[link.p1]
            if link.p2 in self.netHostsPic:
                e1 = self.netHostsPic[link.p2]
            elif link.p2 in self.netSwtichsPic:
                e2 = self.netSwtichsPic[link.p2]
            if e1 != None and e2 != None:
                new_edge = Edge(self.screne, e1, e2)
                # 保存连接线
                new_edge.store()
        self._ui.stack_1.netCalUi.nets.setScene(self.screne)
        self._ui.stack_1.netCalUi.nets.setEnabled(False)
        

    def _initJobResult(self):
        print("init job result")
        # 去除之前的记录
        self._ui.resultui.hostTabs.clear()
        self._ui.resultui.jobTabs.clear()
        self._ui.resultui.faultTabs.clear()
        self._ui.resultui.showHost.clear()
        # self._ui.resultui.show.setChart(QChart())
        # self._ui.resultui.showCPU.setChart(QChart())
        # self._ui.resultui.showRam.setChart(QChart())
        # self._ui.resultui.showGPU.setChart(QChart())
        self.cpushow = QChartView()
        self._ui.resultui.showHost.addTab(self.cpushow, "CPU利用率")
        self.ramshow = QChartView()
        self._ui.resultui.showHost.addTab(self.ramshow, "内存利用率")
        self.gpushow = QChartView()
        self._ui.resultui.showHost.addTab(self.gpushow, "GPU利用率")
        self.totalshow = QChartView()
        self._ui.resultui.showHost.addTab(self.totalshow, "总体")
        self._ui.resultui.showHost.setCurrentIndex(0)
        self._ui.resultui.faultResult.clear()
        self._ui.resultui.jobshow1.clear()
        self._ui.resultui.jobshow2.clear()
        self._ui.resultui.jobShow3.clear()
        # self._ui.resultui.jobResultAnalysis.setChart(QChart())

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
        print("host size: ", len(self.cluster_result.hostRecords))
        print("job size: ", len(self.job_results))
        print("fault size: ", len(self.fault_results))

        self.reliable = xmlParser.parseReliabilityRecord()
        print("reliable: ", self.reliable)
        # 保留两位小数
        self.reliable = round(self.reliable, 2)
    
        otherFormat = '<font color="white" size="5">{}</font>'
        numFormat = '<font color="skyblue" size="20">{}</font>'

        self._ui.resultui.faultResult.setReadOnly(True)
        self._ui.resultui.faultResult.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 字体大，天蓝色
        self._ui.resultui.faultResult.append(numFormat.format(str(self.reliable * 100) + "%"))

        

        self.avergaeRunTime = 0.0
        for job in self.job_results:
            self.avergaeRunTime += getAverageRunTime(job)
        if len(self.job_results) > 0:
            self.avergaeRunTime /= len(self.job_results)
        self.avergaeRunTime = round(self.avergaeRunTime, 2)
        # 不可编辑
        self._ui.resultui.jobshow1.setReadOnly(True)
        self._ui.resultui.jobshow1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 字体大，天蓝色
        self._ui.resultui.jobshow1.append(numFormat.format(str(self.avergaeRunTime))) 
        self._ui.resultui.jobshow1.append(otherFormat.format('s')) 

        self.throughput = (int)(getThroughput(self.job_results, self.cluster_result))
        # self._ui.resultui.jobshow2.setText(str(self.throughput) + "FLOPS/s")
        # 不可编辑
        self._ui.resultui.jobshow2.setReadOnly(True)
        self._ui.resultui.jobshow2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 数字字体大，单位字体小，天蓝色
        # font = QFont()
        # font.setPointSize(20)
        # self._ui.resultui.jobshow2.setStyleSheet("color:skyblue")
        # self._ui.resultui.jobshow2.setFont(font)
        
        # Append different texts
        self._ui.resultui.jobshow2.append(numFormat.format(str(self.throughput))) 
        self._ui.resultui.jobshow2.append(otherFormat.format('TFLOPS/s')) 


        self.efficiency = round(getEfficiency(self.job_results, self.cluster_result), 2)
        # self._ui.resultui.jobshow3.setText(str(self.efficiency))
        # 不可编辑
        self._ui.resultui.jobShow3.setReadOnly(True)
        self._ui.resultui.jobShow3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 字体大，天蓝色
        self._ui.resultui.jobShow3.append(numFormat.format(str(self.efficiency * 100)))
        self._ui.resultui.jobShow3.append(otherFormat.format('%'))




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
        self.hostMore = QTableWidget()
        self.hostMore.verticalHeader().setVisible(False)
        self.hostMore.horizontalHeader().setVisible(True)
        self.hostMore.setColumnCount(4)
        self.hostMore.setHorizontalHeaderLabels(["时间", "CPU(%)", "内存(%)", "GPU(%)"])
        self._ui.resultui.hostTabs.addTab(self.hostMore, "主机详细信息")

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
        self.faultTable.setColumnCount(5)
        self.faultTable.setRowCount(fault_num)
        self.faultTable.setHorizontalHeaderLabels(["时间", "故障对象", "类型", "故障硬件",""])
        i = 0
        for faultRecord in self.fault_results:
            seeMore = QPushButton()
            seeMore.setText("查看")
            seeMore.clicked.connect(partial(self._initFaultResult, faultRecord))
            self.faultTable.setItem(i, 0, QTableWidgetItem(faultRecord.time))
            self.faultTable.setItem(i, 1, QTableWidgetItem(faultRecord.object))
            self.faultTable.setItem(i, 2, QTableWidgetItem(faultRecord.type))
            if faultRecord.hardware == "CPU" or faultRecord.hardware == "cpu":
                self.faultTable.setItem(i, 3, QTableWidgetItem("CPU"))
            elif faultRecord.hardware == "ram" or faultRecord.hardware == "RAM" or faultRecord.hardware == "内存":
                self.faultTable.setItem(i, 3, QTableWidgetItem("内存"))
            elif faultRecord.hardware == "GPU" or faultRecord.hardware == "gpu":
                self.faultTable.setItem(i, 3, QTableWidgetItem("GPU"))
            else:
                self.faultTable.setItem(i, 3, QTableWidgetItem("\\"))
            self.faultTable.setCellWidget(i, 4, seeMore)
            i += 1
        self._ui.resultui.faultTabs.addTab(self.faultTable, "故障记录")
        self.faultMoreTable = QTableWidget()
        # 设置不可见
        self.faultMoreTable.verticalHeader().setVisible(False)
        self.faultMoreTable.horizontalHeader().setVisible(True)
        self.faultMoreTable.setColumnCount(5)
        self.faultMoreTable.setRowCount(0)
        self.faultMoreTable.setHorizontalHeaderLabels(["是否虚警", "重构成功", "可靠度(前)", "可靠度(后)", "资源可用性"])
        self._ui.resultui.faultTabs.addTab(self.faultMoreTable, "故障详细信息")

    def _initChartView(self, hostName):
        chart = self.painter.plotHostUtilization(hostName, -1, float("inf"))
        self.totalshow.setChart(chart)
        chartCPU = self.painter.plotHostCPUUtilization(hostName, -1, float("inf"))
        self.cpushow.setChart(chartCPU)
        chartRam = self.painter.plotHostRamUtilization(hostName, -1, float("inf"))
        self.ramshow.setChart(chartRam)
        chartGPU = self.painter.plotGpuUtilization(hostName, -1, -1, float("inf"))
        self.gpushow.setChart(chartGPU)
        hostR = None
        for hostRecord in self.cluster_result.hostRecords:
            if hostRecord.hostName == hostName:
                hostR = hostRecord
                break
        if hostR == None:
            return
        self.hostMore.setRowCount(len(hostR.hostUtilizations))
        for i in range(len(hostR.hostUtilizations)):
            self.hostMore.setItem(i, 0, QTableWidgetItem(hostR.hostUtilizations[i].time))

            self.hostMore.setItem(i, 1, QTableWidgetItem(str(100 * float(hostR.hostUtilizations[i].cpuUtilization))))
            self.hostMore.setItem(i, 2, QTableWidgetItem(str(100 *float(hostR.hostUtilizations[i].ramUtilization))))
            gpuStr = ""
            for gpu in hostR.hostUtilizations[i].gpuUtilizations:
                gpuStr += str(100 * float(gpu.utilization)) + "/"
            self.hostMore.setItem(i, 3, QTableWidgetItem(gpuStr))
        self._ui.resultui.hostTabs.setCurrentIndex(1)

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
            self.faultMoreTable.setItem(0, 4, QTableWidgetItem("\\"))
            self._ui.resultui.faultTabs.setCurrentIndex(1)
            return
        else:
            if faultRecord.isSuccessRebuild == "True":
                self.faultMoreTable.setItem(0, 1, QTableWidgetItem("是"))
            else:
                self.faultMoreTable.setItem(0, 1, QTableWidgetItem("否"))
            self.faultMoreTable.setItem(0, 2, QTableWidgetItem(str(faultRecord.redundancyBefore)))
            self.faultMoreTable.setItem(0, 3, QTableWidgetItem(str(faultRecord.redundancyAfter)))
            self.faultMoreTable.setItem(0, 4, QTableWidgetItem(str(faultRecord.redundancyAfter)))
        self._ui.resultui.faultTabs.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv+["--no-sandbox"])
    print(sys.argv)
    win = None
    # if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):  # Enable High DPI display with Qt5
    #     app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    # QDir.addSearchPath("icons", f"{get_project_root_path().as_posix()}/widget_gallery/ui/svg")
    if len(sys.argv) <2:
        if getattr(sys, 'frozen', False):
            win = JobSimQt(os.path.dirname(sys.executable)  + "/project", -1)
        else:
            win = JobSimQt(os.path.dirname(os.path.abspath(__file__)) + "/project", -1)
    elif len(sys.argv) == 2:
        if getattr(sys, 'frozen', False):
            win = JobSimQt(os.path.dirname(sys.executable)  + "/project", sys.argv[1])
        else:
            win = JobSimQt(os.path.dirname(os.path.abspath(__file__)) + "/project", int(sys.argv[1]))
    else:
        win = JobSimQt(sys.argv[1], int(sys.argv[2]))
    win.menuBar().setNativeMenuBar(False)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    win.show()
    app.exec()
