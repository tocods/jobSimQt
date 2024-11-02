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
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot, QRegularExpression, QUrl
from qdarktheme.qtpy.QtGui import *
from qdarktheme.qtpy.QtWidgets import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtNetwork import QNetworkCookie
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
import globaldata
class JobSimQt(QMainWindow):
    def __init__(self, path) -> None:
        super().__init__()
        self.duration = 100
        project.projectPath = path
        globaldata.currentProjectInfo.setRelativePath(path)
        self._initOutputFiles()
        # 取消标题栏
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.nowClect = None
        self._ui = UI()
        self._ui.setup_ui(self)
        self._ui.stack_widget.setCurrentIndex(0)
        # Signal
        self._ui.action_change_home.triggered.connect(self._change_page)
        self._ui.action_change_dock.triggered.connect(self._change_page)
        self._ui.action_micro_service.triggered.connect(self._change_page)
        self._ui.action_net_safe.triggered.connect(self._change_page)
        self._ui.action_open_folder.triggered.connect(self.loadFromProject
            #lambda: QFileDialog.getOpenFileName(self, "Open File", options=QFileDialog.Option.DontUseNativeDialog)
        )
        self._ui.action_out.triggered.connect(sys.exit)
        # self._ui.action_enable.triggered.connect(self._toggle_state)
        # self._ui.action_disable.triggered.connect(self._toggle_state)
        for action in self._ui.actions_theme:
            action.triggered.connect(self._change_theme)
        screen = QGuiApplication.screens()[0]
        screen_size = screen.availableGeometry()
        self.setGeometry(0, 0, screen_size.width() * 0.9, screen_size.height() * 0.9)
        self._ui.resultui.layoutWidget.setGeometry(0, 0, screen_size.width() * 0.8, screen_size.height() * 0.8)
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
            self._ui.stack_widget.setCurrentIndex(1)
        if action_name == "微服务指标采集":
                    # 初始化一个page
            self.webview = QWebEngineView(self._ui.stack_3)
            self.weburl="http://localhost:3000/d/IV0hu1m7z/windows-exporter-dashboard?orgId=1"
            #self.save_cookies()
            #self.load_cookies()
            # 加载一个网页，以便产生一些 cookies
            self.webview.page().load(QUrl(self.weburl))
            #self.cookie_store.cookieAdded.connect(self.handlecookie))
            #页面加载完成执行
            #self.view.page().loadFinished.connect(self.on_page_load_finished)
            screen = QGuiApplication.screens()[0]
            screen_size = screen.availableGeometry()
            self._ui.stack_3.setGeometry(0, 0, screen_size.width() * 0.8, screen_size.height() * 0.8)
            self.webview.setGeometry(0, 0, screen_size.width() * 0.8, screen_size.height() * 0.8)
            self._ui.stack_widget.setCurrentIndex(2)
        if action_name == "网络安全评估":
            os.popen("D:\\NetworkDataSecurityAssessment\\NetworkDataSecurityAssessment.exe")
    
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

    def saveToProject(self):
       return

    def loadFromProject(self):
        file_name = QFileDialog.getExistingDirectory(None, "Open File", "")
        print(file_name)
        project.projectPath = file_name
        self._initOutputFiles()
        self._ui.stack_widget.setCurrentIndex(1)
        self._ui.resultui.hostTabs.clear()
        self._ui.resultui.jobTabs.clear()
        self._ui.resultui.faultTabs.clear()
        self._ui.resultui.show.setChart(QChart())
        self._ui.resultui.showCPU.setChart(QChart())
        self._ui.resultui.showRam.setChart(QChart())
        self._ui.resultui.showGPU.setChart(QChart())
        self._ui.resultui.faultResultAnalysis.setChart(QChart())
        self._ui.resultui.jobResultAnalysis.setChart(QChart())
        self._initAll()
        #self.setClicked()
    
    def _initOutputFiles(self):
        if not os.path.exists(project.projectPath + "/OutputFiles/hostUtils.xml"):
            with open(project.projectPath + "/OutputFiles/hostUtils.xml", "w") as f:
                f.write("")
        if not os.path.exists(project.projectPath + "/OutputFiles/jobRun.xml"):
            with open(project.projectPath + "/OutputFiles/jobRun.xml", "w") as f:
                f.write("")
        if not os.path.exists(project.projectPath + "/OutputFiles/faultRecords.xml"):
            with open(project.projectPath + "/OutputFiles/faultRecords.xml", "w") as f:
                f.write("")
    
    def _initAll(self):
        print("init all")
        print(project.projectPath)
        sysSim.hosts = {}
        sysSim.jobs = {}
        sysSim.faults = {}
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
        self._initJobResult()

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
        self._ui.resultui.faultResultAnalysis.setChart(QChart())
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

        # chart = QChart()
        # chart.addSeries(self.jobSeries)
        # chart.setTitle("计算效率\n" + str(percent_total * 100) + "%")
        # chart.legend().hide()
        # self._ui.resultui.jobResultAnalysis.setChart(chart)
        # # 抗锯齿
        # self._ui.resultui.jobResultAnalysis.setRenderHint(QPainter.Antialiasing)
        # self._ui.resultui.jobResultAnalysis.setRenderHint(QPainter.TextAntialiasing)

        self.avergaeRunTime = 0.0
        for job in self.job_results:
            self.avergaeRunTime += getAverageRunTime(job)
        self.avergaeRunTime /= len(self.job_results)
        self.avergaeRunTime = round(self.avergaeRunTime, 2)
        self.pieSeries = QPieSeries()
        self.pieSeries.append("平均运行\n" + str(self.avergaeRunTime) + "s", self.avergaeRunTime)
        self.pieSeries.append(":" + str(self.duration - self.avergaeRunTime) + "s", self.duration - self.avergaeRunTime)
        self.pieSeries.setPieSize(0.5)
        self._ui.resultui.jobshow1.setText(str(self.avergaeRunTime) + "s")
        # 不可编辑
        self._ui.resultui.jobshow1.setReadOnly(True)
        self._ui.resultui.jobshow1.setAlignment(Qt.AlignCenter)

        # chart = QChart()
        # chart.addSeries(self.pieSeries)
        # chart.setTitle("平均运行\n" + str(self.avergaeRunTime) + "s")
        # chart.legend().hide()
        # self._ui.resultui.jobResultAnalysis2.setChart(chart)
        # # 抗锯齿
        # self._ui.resultui.jobResultAnalysis2.setRenderHint(QPainter.Antialiasing)
        # self._ui.resultui.jobResultAnalysis2.setRenderHint(QPainter.TextAntialiasing)

        self.throughput = (int)(getThroughput(self.job_results))
        self._ui.resultui.jobshow2.setText(str(self.throughput) + "FLOPS/s")
        # 不可编辑
        self._ui.resultui.jobshow2.setReadOnly(True)
        self.pieSeries = QPieSeries()
        self.pieSeries.append(str(self.throughput) + "FLOPS/s", self.throughput)
        # self.pieSeries.append(":" + str(100 - self.throughput) + "FLOPS/s", 100 - self.throughput)
        self.pieSeries.setPieSize(0.5)

        # chart = QChart()
        # chart.addSeries(self.pieSeries)
        # chart.setTitle("吞吐\n" + str(self.throughput) + "/s")
        # chart.legend().hide()
        # self._ui.resultui.jobResultAnalysis3.setChart(chart)
        # # 抗锯齿
        # self._ui.resultui.jobResultAnalysis3.setRenderHint(QPainter.Antialiasing)
        # self._ui.resultui.jobResultAnalysis3.setRenderHint(QPainter.TextAntialiasing)




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
        self.totalshow.setChart(chart)
        chartCPU = self.painter.plotHostCPUUtilization(hostName, -1, float("inf"))
        self.cpushow.setChart(chartCPU)
        chartRam = self.painter.plotHostRamUtilization(hostName, -1, float("inf"))
        self.ramshow.setChart(chartRam)
        chartGPU = self.painter.plotGpuUtilization(hostName, -1, -1, float("inf"))
        self.gpushow.setChart(chartGPU)

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
