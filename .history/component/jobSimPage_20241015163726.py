from jobSim import JobInfo, TaskInfo, CPUTaskInfo, GPUTaskInfo, FaultGenerator, ParseUtil
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from typing import List, Optional
from terminaltables import AsciiTable
import xml.etree.ElementTree as ET
from functools import partial
import json
import subprocess
from jobSim import sysSim



class JobSimPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initJob()

    def refresh(self):
        # self.l = QFormLayout()
        # #self.setupUi(self.l)
        # self.resize(500, 200)
        # self.setWindowTitle("任务建模")
        # self.job = QLabel("任务建模")
        # self.XMLJob = QPushButton("输入文件")
        # self.XMLJob.setFixedSize(300, 150)
        # self.ListJob = QPushButton("任务列表")
        # self.ListJob.setFixedSize(300, 150)
        # j = QFormLayout()
        # j.addRow(self.XMLJob, self.ListJob)

        # color = QColor(0, 0, 0)
        # style_sheet = "color: {}".format(color.name())
        # self.job.setStyleSheet(style_sheet)
        # self.XMLJob.setStyleSheet(style_sheet)
        # self.ListJob.setStyleSheet(style_sheet)
       
        # self.l.addRow(j)
    
        # self.setupClick()

      
        # self.initJob()


        # self.setLayout(self.l)
        self.setWindowTitle("任务列表")
        
        self.table = QTableWidget(self)
        self.table.setRowCount(len(self.jobs))
        self.table.setColumnCount(3)
        self.setColumnWidthAsProportion(self.table, [1, 5, 5], 1600)
        self.setRowHeightAsNum(self.table, 800)
        self.setFontOfTable(self.table)
        self.paintTable()
        self.addJob = QPushButton("添加任务")
        self.addJob.setFixedSize(600, 60)
        self.addJob.setFont(QFont("Microsoft YaHei", 20))
        self.addJob.clicked.connect(self.addJobClicked)
        self.clearJob = QPushButton("清空任务")
        self.clearJob.clicked.connect(self.clearJobInfo)
        self.clearJob.setFixedSize(600, 60)
        self.clearJob.setFont(QFont("Microsoft YaHei", 20))
        self.layout = QFormLayout()
        sim = QFormLayout()
        sim.addRow(self.addJob, self.clearJob)
        self.layout.addRow(self.table)
        self.layout.addRow(sim)
        self.setLayout(self.layout)

    def paintTable(self):
        print("paintTable")
        self.table.clear()
        #不显示行号和列号
        self.table.verticalHeader().setVisible(False)
        #self.table.horizontalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['任务名', '', ''])
        self.infoJob = []
        self.delJob = []
        for i, job in enumerate(self.jobs):
            self.table.setItem(i, 0, QTableWidgetItem(job.name))
            info = QPushButton("查看")
            info.clicked.connect(partial(self.showJobInfo, job))
            self.infoJob.append(info)
            self.table.setCellWidget(i, 1, info)
            delT = QPushButton("删除")
            delT.clicked.connect(partial(self.delJobInfo, job))
            self.delJob.append(delT)
            self.table.setCellWidget(i, 2, delT)
        self.table.show()
        
        
 

    def initJob(self):
        self.jobs = sysSim.jobs
 
    def setColumnWidthAsProportion(self, table: QTableWidget,proportionList, width):
        for i, proportion in enumerate(proportionList):
            wid = width * proportion / sum(proportionList)
            table.setColumnWidth(i, int(wid))

    def setRowHeightAsNum(self, table: QTableWidget,height: int):
        for i in range(table.rowCount()):
            table.setRowHeight(i, 100)

    def setFontOfTable(self, table: QTableWidget):
        font = QFont()
        font.setPointSize(20)
        table.setFont(font)
        table.horizontalHeader().setFont(font)

    def XMLJobClicked(self):
        jobFile = QFileDialog.getOpenFileName(self, "选择文件") 
        print(jobFile)
        parseUtil = ParseUtil()
        ret = parseUtil.parse_job_xml(jobFile[0])
        self.jobs = parseUtil.get_job_infos()
        jobList = self.jobs
        QMessageBox.information(None, "", "已成功导入")

    def ListJobClicked(self):
        self.JobList = QWidget()
        self.JobList.resize(1600, 1200)
        self.JobList.setWindowTitle("任务列表")
        self.JobList.show()
        self.JobList.table = QTableWidget(self.JobList)
        self.JobList.table.setRowCount(len(self.jobs))
        self.JobList.table.setColumnCount(3)
        self.setColumnWidthAsProportion(self.JobList.table, [1, 5, 5], 1600)
        self.setRowHeightAsNum(self.JobList.table, 800)
        self.setFontOfTable(self.JobList.table)
        self.JobList.table.setHorizontalHeaderLabels(['任务名', '', ''])
        self.infoJob = []
        self.delJob = []
        for i, job in enumerate(self.jobs):
            self.JobList.table.setItem(i, 0, QTableWidgetItem(job.name))
            info = QPushButton("查看")
            info.clicked.connect(partial(self.showJobInfo, job))
            self.infoJob.append(info)
            self.JobList.table.setCellWidget(i, 1, info)
            delT = QPushButton("删除")
            delT.clicked.connect(partial(self.delJobInfo, job))
            self.delJob.append(delT)
            self.JobList.table.setCellWidget(i, 2, delT)
        self.JobList.table.show()
        self.addJob = QPushButton("添加任务")
        self.addJob.setFixedSize(600, 60)
        self.addJob.setFont(QFont("Microsoft YaHei", 20))
        self.addJob.clicked.connect(self.addJobClicked)
        self.clearJob = QPushButton("清空任务")
        self.clearJob.clicked.connect(self.clearJobInfo)
        self.clearJob.setFixedSize(600, 60)
        self.clearJob.setFont(QFont("Microsoft YaHei", 20))
        self.JobList.layout = QFormLayout()
        sim = QFormLayout()
        sim.addRow(self.addJob, self.clearJob)
        self.JobList.layout.addRow(self.JobList.table)
        self.JobList.layout.addRow(sim)
        self.JobList.setLayout(self.JobList.layout)
        self.JobList.show()

    def delJobInfo(self, job: JobInfo):
        
        self.jobs.remove(job)
        self.table.removeRow(self.table.currentRow())
        sysSim.jobs = self.jobs

    def clearJobInfo(self):
        self.jobs.clear()
        self.table.clear()
        sysSim.jobs = self.jobs

    def addJobClicked(self):
        #self.JobList.hide()
        self.addJob = QWidget()
        self.addJob.setWindowTitle("添加任务")
        self.addJob.show()
        self.addJob.resize(1600, 1200)
        self.addJob.table = QTableWidget(self.addJob)
        self.addJob.table.verticalHeader().setVisible(False)
        self.addJob.table.horizontalHeader().setVisible(False)
        self.addJob.table.setRowCount(5)
        self.addJob.table.setColumnCount(7)
        self.setColumnWidthAsProportion(self.addJob.table, [1, 1, 1, 1, 1, 1, 1], 1600)
        self.setRowHeightAsNum(self.addJob.table, 1000)
        self.setFontOfTable(self.addJob.table)
        self.addJob.table.setItem(0,0, QTableWidgetItem("任务名"))
        self.addJob.table.setItem(0,1, QTableWidgetItem("任务周期(秒)"))
        self.addJob.table.setItem(0,2, QTableWidgetItem("需求内存大小(MB)"))
        #self.addJob.table.setItem(0,3, QTableWidgetItem("需求显存大小(MB)"))
        self.addJob.name_edit = QLineEdit()
        #self.addJob.name_edit.setPlaceholderText("任务名")
        self.addJob.table.setCellWidget(1, 0, self.addJob.name_edit)
        self.addJob.period_edit = QLineEdit()
        #self.addJob.period_edit.setPlaceholderText("任务周期")
        self.addJob.table.setCellWidget(1, 1, self.addJob.period_edit)
        self.addJob.ram_edit = QLineEdit()
        #self.addJob.ram_edit.setPlaceholderText("内存大小")
        self.addJob.table.setCellWidget(1, 2, self.addJob.ram_edit)
        self.addJob.gddram_edit = QLineEdit()
        #self.addJob.gddram_edit.setPlaceholderText("显存大小")
        #self.addJob.table.setCellWidget(1, 3, self.addJob.gddram_edit)
        self.addJob.table.setItem(2,0, QTableWidgetItem("需求CPU核数"))
        self.addJob.table.setItem(2,1, QTableWidgetItem("CPU部分FLOP"))
        self.addJob.cpu_cores_edit = QLineEdit()
        #self.addJob.cpu_cores_edit.setPlaceholderText("CPU核数")
        self.addJob.table.setCellWidget(3, 0, self.addJob.cpu_cores_edit)
        self.addJob.cpu_flop_edit = QLineEdit()
        #self.addJob.cpu_flop_edit.setPlaceholderText("FLOP")
        self.addJob.kernel_num = 0
        self.addJob.table.setCellWidget(3, 1, self.addJob.cpu_flop_edit)
        self.addJob.table.setItem(4,0, QTableWidgetItem("GPU内核"))
        self.addJob.table.setItem(4,1, QTableWidgetItem("线程块数"))
        self.addJob.table.setItem(4,2, QTableWidgetItem("线程数/线程块"))
        self.addJob.table.setItem(4,3, QTableWidgetItem("FLOP/线程"))
        self.addJob.table.setItem(4,4, QTableWidgetItem("输入大小(MB)"))
        self.addJob.table.setItem(4,5, QTableWidgetItem("输出大小(MB)"))
        self.addJob.table.setItem(4,6, QTableWidgetItem("需求显存大小(MB)"))
        self.addJob.table.setItem(5,0, QTableWidgetItem("1"))
        self.addJob.block_num_edits = []
        self.addJob.thread_num_edits = []
        self.addJob.flop_edits = []
        self.addJob.io_in_edits = []
        self.addJob.io_out_edits = []
        self.addJob.gddram_edits = []

        #block_num_edit = QLineEdit()
        
        # self.addJob.table.setCellWidget(5, 1, block_num_edit)
        # self.addJob.block_num_edits.append(block_num_edit)
        
        # thread_num_edit = QLineEdit()
        
        # self.addJob.table.setCellWidget(5, 2, thread_num_edit)
        # self.addJob.thread_num_edits.append(thread_num_edit)
        
        # flop_edit = QLineEdit()
        
        # self.addJob.table.setCellWidget(5, 3, flop_edit)
        # self.addJob.flop_edits.append(flop_edit)
        
        # io_in_edit = QLineEdit()
        
        # self.addJob.table.setCellWidget(5, 4, io_in_edit)
        # self.addJob.io_in_edits.append(io_in_edit)
        
        # io_out_edit = QLineEdit()
        
        # self.addJob.table.setCellWidget(5, 5, io_out_edit)
        # self.addJob.io_out_edits.append(io_out_edit)
        self.addJob.add = QPushButton("应用", self.addJob)
        self.addJob.add.setFixedSize(600, 60)
        self.addJob.add.setFont(QFont("Microsoft YaHei", 20))
        self.addJob.add.clicked.connect(self.addJobInfo)
        self.addJob.addKernel = QPushButton("添加内核", self.addJob)
        self.addJob.addKernel.setFixedSize(600, 60)
        self.addJob.addKernel.setFont(QFont("Microsoft YaHei", 20))
        self.addJob.addKernel.clicked.connect(self.addKernel)
        self.addJob.layout = QFormLayout()
        self.addJob.layout.addRow(self.addJob.table)
        self.addJob.layout.addRow(self.addJob.addKernel, self.addJob.add)
        self.addJob.setLayout(self.addJob.layout)
        self.addJob.show()
        self.addJob.table.show()
        self.addJob.add.show()
        

    def addJobInfo(self):
        job = JobInfo()
        job.name = self.addJob.name_edit.text()
        job.period = float(self.addJob.period_edit.text())
        job.cpu_task = CPUTaskInfo(int(self.addJob.ram_edit.text()), int(self.addJob.cpu_cores_edit.text()), int(self.addJob.cpu_flop_edit.text()))
        kernels = []
        taskInputSize = 0
        taskOutputSize = 0
        requestedGddram = 0
        for i in range(self.addJob.kernel_num):
            kernels.append(GPUTaskInfo.Kernel(int(self.addJob.block_num_edits[i].text()), int(self.addJob.thread_num_edits[i].text()), float(self.addJob.flop_edits[i].text())))
            taskInputSize += int(self.addJob.io_in_edits[i].text())
            taskOutputSize += int(self.addJob.io_out_edits[i].text())
            requestedGddram += int(self.addJob.gddram_edits[i].text())
        if len(kernels) > 0: 
            job.gpu_task = GPUTaskInfo(kernels, task_input_size=taskInputSize, task_output_size=taskOutputSize)
            job.gpu_task.requested_gddram_size = requestedGddram
        else:
            job.gpu_task = None 
        #job.gpu_task.task_input_size = int(self.addJob.io_in_edit.text())
        #job.gpu_task.task_output_size = int(self.addJob.io_out_edit.text())
        self.jobs.append(job)
        sysSim.jobs = self.jobs
        job.print()
        #self.JobList.hide()
        #self.ListJobClicked()
        self.addJob.hide()
        self.table.setRowCount(len(self.jobs))
        self.setRowHeightAsNum(self.table, 1000)
        i = len(self.jobs) - 1
        self.table.setItem(i, 0, QTableWidgetItem(job.name))
        info = QPushButton("查看")
        info.clicked.connect(partial(self.showJobInfo, job))
        self.infoJob.append(info)
        self.table.setCellWidget(i, 1, info)
        delT = QPushButton("删除")
        delT.clicked.connect(partial(self.delJobInfo, job))
        self.delJob.append(delT)
        self.table.setCellWidget(i, 2, delT)

    def addKernel(self):
        self.addJob.kernel_num += 1
        self.addJob.table.setRowCount(self.addJob.table.rowCount() + 1)
        self.setColumnWidthAsProportion(self.addJob.table, [1, 1, 1, 1, 1, 1], 1600)
        self.setRowHeightAsNum(self.addJob.table, 1000)
        self.addJob.table.setItem(5 + self.addJob.kernel_num - 1, 0, QTableWidgetItem(str(self.addJob.kernel_num)))
        block_num_edit = QLineEdit()
        #self.addJob.block_num_edit.setPlaceholderText("线程块数")
        self.addJob.table.setCellWidget(5 + self.addJob.kernel_num - 1, 1, block_num_edit)
        self.addJob.block_num_edits.append(block_num_edit)
        thread_num_edit = QLineEdit()
        #self.addJob.thread_num_edit.setPlaceholderText("线程数/线程块")
        self.addJob.table.setCellWidget(5 + self.addJob.kernel_num - 1, 2, thread_num_edit)
        self.addJob.thread_num_edits.append(thread_num_edit)
        flop_edit = QLineEdit()
        #self.addJob.flop_edit.setPlaceholderText("FLOP/线程")
        self.addJob.table.setCellWidget(5 + self.addJob.kernel_num - 1, 3, flop_edit)
        self.addJob.flop_edits.append(flop_edit)
        io_in_edit = QLineEdit()
        #self.addJob.io_in_edit.setPlaceholderText("输入大小")
        self.addJob.table.setCellWidget(5 + self.addJob.kernel_num - 1, 4, io_in_edit)
        self.addJob.io_in_edits.append(io_in_edit)
        io_out_edit = QLineEdit()
        #self.addJob.io_out_edit.setPlaceholderText("输出大小")
        self.addJob.table.setCellWidget(5 + self.addJob.kernel_num - 1, 5, io_out_edit)
        self.addJob.io_out_edits.append(io_out_edit)
        gddram_edit = QLineEdit()
        #self.addJob.gddram_edit.setPlaceholderText("显存大小")
        self.addJob.table.setCellWidget(5 + self.addJob.kernel_num - 1, 6, gddram_edit)
        self.addJob.gddram_edits.append(gddram_edit)


    def showJobInfo(self, job: JobInfo):
        self.JobInfo = QTableWidget()
        self.JobInfo.setWindowTitle("任务信息")
        self.JobInfo.verticalHeader().setVisible(False)
        self.JobInfo.horizontalHeader().setVisible(False)
        self.JobInfo.resize(1600, 1200)
        if job.gpu_task is not None:
            self.JobInfo.setRowCount(5 + len(job.gpu_task.kernels))
        else:
            self.JobInfo.setRowCount(4)
        self.JobInfo.setColumnCount(6)
        self.setColumnWidthAsProportion(self.JobInfo, [1, 1, 1, 1, 1, 1], 1600)
        self.setRowHeightAsNum(self.JobInfo, 1000)
        self.setFontOfTable(self.JobInfo)
        self.JobInfo.setItem(0, 0, QTableWidgetItem("任务名"))
        self.JobInfo.setItem(0, 1, QTableWidgetItem("任务周期(秒)"))
        self.JobInfo.setItem(0, 2, QTableWidgetItem("内存大小(MB)"))
        self.JobInfo.setItem(1, 0, QTableWidgetItem(job.name))
        self.JobInfo.setItem(1, 1, QTableWidgetItem(str(job.period)))
        self.JobInfo.setItem(1, 2, QTableWidgetItem(str(job.cpu_task.ram)))
        self.JobInfo.setItem(2, 0, QTableWidgetItem("需求CPU核数"))
        self.JobInfo.setItem(2, 1, QTableWidgetItem("CPU部分FLOP"))
        self.JobInfo.setItem(3, 0, QTableWidgetItem(str(job.cpu_task.pes_number)))
        self.JobInfo.setItem(3, 1, QTableWidgetItem(str(job.cpu_task.length)))
        if job.gpu_task is not None:
            self.JobInfo.setItem(4, 0, QTableWidgetItem("GPU内核"))
            self.JobInfo.setItem(4, 1, QTableWidgetItem("线程块数"))
            self.JobInfo.setItem(4, 2, QTableWidgetItem("线程数数/线程块"))
            self.JobInfo.setItem(4, 3, QTableWidgetItem("FLOP/线程"))
            for i, kernel in enumerate(job.gpu_task.kernels):
                self.JobInfo.setItem(5 + i, 0, QTableWidgetItem(str(i)))
                self.JobInfo.setItem(5 + i, 1, QTableWidgetItem(str(kernel.block_num)))
                self.JobInfo.setItem(5 + i, 2, QTableWidgetItem(str(kernel.thread_length)))
                self.JobInfo.setItem(5 + i, 3, QTableWidgetItem(str(kernel.thread_length)))
        self.JobInfo.show()
