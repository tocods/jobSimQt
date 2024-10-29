from qdarktheme.qtpy.QtCore import Qt
from qdarktheme.qtpy.QtWidgets import *
from qdarktheme.qtpy.QtCore import *
from qdarktheme.qtpy.QtGui import *
from qdarktheme.qtpy.QtWidgets import QWidget

from item import GraphicItem
from jobSim import HostInfo, CPUInfo, GPUInfo, VideoCardInfo, jobSim
from globaldata import hostList

class HostInfoForm(QMainWindow):
    def __init__(self, jobSim:jobSim, parent = None):
        super().__init__(parent)
        self.jobSim = jobSim
    
    def showItem(self, item: GraphicItem):
        onlyCpu = self.jobSim.onlyCPU[item]
        self.item = item
        host = self.jobSim.getHostInfo(item)
        print(host)
        self.addHost = QWidget()
        self.addHost.resize(1600, 1200)
        self.addHost.cpu_num = len(host.cpu_infos)
        if(len(host.video_card_infos) == 0):
            self.addHost.gpu_num = 0
        else:
            self.addHost.gpu_num = len(host.video_card_infos[0].gpu_infos)
        self.addHost.setWindowTitle("添加主机")
        self.addHost.show()
        self.addHost.table = QTableWidget(self.addHost)
        # self.addHost.table.resize
        self.addHost.table.setRowCount(4+self.addHost.cpu_num+self.addHost.gpu_num)
        self.addHost.table.setColumnCount(5)
        self.setFontOfTable(self.addHost.table)
        self.setColumnWidthAsProportion(self.addHost.table, [1, 1, 1, 1, 1], 1600)
        self.setRowHeightAsNum(self.addHost.table, 1000)
        self.addHost.table.setItem(0,0, QTableWidgetItem("主机名"))
        self.addHost.table.setItem(0,1, QTableWidgetItem("内存大小(MB)"))
        self.addHost.table.setItem(0,2, QTableWidgetItem("PCIe带宽(Gbps)"))
        self.addHost.table.gpu_share = QRadioButton("GPU共享")  
        self.addHost.table.gpu_share.setChecked(True)
        self.addHost.table.setItem(0,3, QTableWidgetItem("GPU共享"))
        # self.addHost.name = QLineEdit()
        # self.addHost.name.setText(host.name)
        # self.addHost.table.setCellWidget(1, 0, self.addHost.name)
        self.addHost.table.setCellWidget(1, 0, QLabel(host.name))
        self.addHost.ram = QLineEdit()
        self.addHost.ram.setText(str(host.ram))
        self.addHost.table.setCellWidget(1, 1, self.addHost.ram)
        self.addHost.pcie = QLineEdit()
        if len(host.video_card_infos) > 0:
            self.addHost.pcie.setText(str(host.video_card_infos[0].pcie_bw))
        self.addHost.table.setCellWidget(1, 2, self.addHost.pcie)
        self.addHost.table.setCellWidget(1, 3, self.addHost.table.gpu_share)
        #self.addHost.table.setItem(2,0, QTableWidgetItem("CPU数"))
        self.addHost.table.setItem(2,0, QTableWidgetItem("CPU核数"))
        self.addHost.table.setItem(2,1, QTableWidgetItem("核FLOPS"))
        self.addHost.cpu_flops_edits = []
        self.addHost.cpu_cores_edits = []
        for i, cpu in enumerate(host.cpu_infos):
            cpu_cores_edit = QLineEdit()
            cpu_cores_edit.setText(str(cpu.cores))
            self.addHost.cpu_cores_edits.append(cpu_cores_edit)
            self.addHost.table.setCellWidget(3 + i, 0, cpu_cores_edit)
            cpu_flops_edit = QLineEdit()
            cpu_flops_edit.setText(str(cpu.mips))
            self.addHost.cpu_flops_edits.append(cpu_flops_edit)
            self.addHost.table.setCellWidget(3 + i, 1, cpu_flops_edit)
        if not onlyCpu:
            self.addHost.table.setItem(3 + self.addHost.cpu_num,0, QTableWidgetItem("GPU核数"))
            self.addHost.table.setItem(3 + self.addHost.cpu_num,1, QTableWidgetItem("GPU SM数"))
            self.addHost.table.setItem(3 + self.addHost.cpu_num,2, QTableWidgetItem("GPU最大线程块数/SM"))
            self.addHost.table.setItem(3 + self.addHost.cpu_num,3, QTableWidgetItem("GPU核FLOPS"))
            self.addHost.table.setItem(3 + self.addHost.cpu_num,4, QTableWidgetItem("GPU显存(MB)"))
        self.addHost.gpu_cores_edits = []
        self.addHost.gpu_sm_edits = []
        self.addHost.gpu_max_block_edits = []
        self.addHost.gpu_flops_edits = []
        self.addHost.gpu_mem_edits = []
        if len(host.video_card_infos) > 0:
            for i, gpu in enumerate(host.video_card_infos[0].gpu_infos):
                gpu_cores_edit = QLineEdit()
                gpu_cores_edit.setText(str(gpu.cores))
                self.addHost.gpu_cores_edits.append(gpu_cores_edit)
                self.addHost.table.setCellWidget(4 + self.addHost.cpu_num, 0, gpu_cores_edit)
                gpu_sm_edit = QLineEdit()
                gpu_sm_edit.setText(str(gpu.core_per_sm))
                self.addHost.gpu_sm_edits.append(gpu_sm_edit)
                self.addHost.table.setCellWidget(4 + self.addHost.cpu_num, 1, gpu_sm_edit)
                gpu_max_block_edit = QLineEdit()
                gpu_max_block_edit.setText(str(gpu.max_block_per_sm))
                self.addHost.gpu_max_block_edits.append(gpu_max_block_edit)
                self.addHost.table.setCellWidget(4 + self.addHost.cpu_num, 2, gpu_max_block_edit)
                gpu_flops = QLineEdit()
                gpu_flops.setText(str(gpu.flops_per_core))
                self.addHost.gpu_flops_edits.append(gpu_flops)
                self.addHost.table.setCellWidget(4 + self.addHost.cpu_num, 3, gpu_flops)
                gpu_mem = QLineEdit()
                gpu_mem.setText(str(gpu.gddram))
                self.addHost.gpu_mem_edits.append(gpu_mem)
                self.addHost.table.setCellWidget(4 + self.addHost.cpu_num, 4, gpu_mem)
        # self.addHost.table.resizeColumnsToContents()
        # self.addHost.table.resizeRowsToContents()
        self.addHost.add = QPushButton("应用", self.addHost)
        self.addHost.add.setFixedSize(600, 60)
        self.addHost.add.setFont(QFont("Microsoft YaHei", 20))
        self.addHost.add.clicked.connect(self.addHostInfo)
        if not onlyCpu:
            self.addHost.gpu = QPushButton("增加GPU")
            self.addHost.gpu.setFixedSize(600, 60)
            self.addHost.gpu.setFont(QFont("Microsoft YaHei", 20))
            self.addHost.gpu.clicked.connect(self.addGPU)
        self.addHost.cpu = QPushButton("增加CPU")
        self.addHost.cpu.setFixedSize(600, 60)
        self.addHost.cpu.setFont(QFont("Microsoft YaHei", 20))
        self.addHost.cpu.clicked.connect(self.addCPU)
        self.addHost.layout = QFormLayout()
        self.addHost.layout.addRow(self.addHost.table)
        if not onlyCpu:
            self.addHost.layout.addRow(self.addHost.cpu, self.addHost.gpu)
        else:
            self.addHost.layout.addRow(self.addHost.cpu)
        self.addHost.layout.addRow(self.addHost.add)
        self.addHost.setLayout(self.addHost.layout)
        #self.addHost.show()
        #self.addHost.table.show()
        #self.addHost.add.show()

    def addGPU(self):
        self.addHost.table.insertRow(self.addHost.table.rowCount())
        self.addHost.gpu_num += 1
        self.setFontOfTable(self.addHost.table)
        self.setColumnWidthAsProportion(self.addHost.table, [1, 1, 1, 1, 1], 1600)
        self.setRowHeightAsNum(self.addHost.table, 1000)
        gpu_cores_edit = QLineEdit()
        gpu_cores_edit.setText(str(1000))
        self.addHost.gpu_cores_edits.append(gpu_cores_edit)
        self.addHost.table.setCellWidget(3 + self.addHost.cpu_num + self.addHost.gpu_num, 0, gpu_cores_edit)
        gpu_sm_edit = QLineEdit()
        gpu_sm_edit.setText(str(100))
        self.addHost.gpu_sm_edits.append(gpu_sm_edit)
        self.addHost.table.setCellWidget(3 + self.addHost.cpu_num + self.addHost.gpu_num, 1, gpu_sm_edit)
        gpu_max_block_edit = QLineEdit()
        gpu_max_block_edit.setText(str(10))
        self.addHost.gpu_max_block_edits.append(gpu_max_block_edit)
        self.addHost.table.setCellWidget(3 + self.addHost.cpu_num + self.addHost.gpu_num, 2, gpu_max_block_edit)
        gpu_flops = QLineEdit()
        gpu_flops.setText(str(100))
        self.addHost.gpu_flops_edits.append(gpu_flops)
        self.addHost.table.setCellWidget(3 + self.addHost.cpu_num + self.addHost.gpu_num, 3, gpu_flops)
        gpu_mem = QLineEdit()
        gpu_mem.setText(str(1000))
        self.addHost.gpu_mem_edits.append(gpu_mem)
        self.addHost.table.setCellWidget(3 + self.addHost.cpu_num + self.addHost.gpu_num, 4, gpu_mem)

    def addCPU(self):
        self.addHost.table.insertRow(3 + self.addHost.cpu_num)
        self.addHost.cpu_num += 1
        self.setFontOfTable(self.addHost.table)
        self.setColumnWidthAsProportion(self.addHost.table, [1, 1, 1, 1], 1600)
        self.setRowHeightAsNum(self.addHost.table, 1000)
        cpu_cores_edit = QLineEdit()
        cpu_cores_edit.setText(str(1))
        self.addHost.cpu_cores_edits.append(cpu_cores_edit)
        self.addHost.table.setCellWidget(2 + self.addHost.cpu_num, 0, cpu_cores_edit)
        cpu_flops_edit = QLineEdit()
        cpu_flops_edit.setText(str(1000))
        self.addHost.cpu_flops_edits.append(cpu_flops_edit)
        self.addHost.table.setCellWidget(2 + self.addHost.cpu_num, 1, cpu_flops_edit)

    def addHostInfo(self):
        host = HostInfo()
        #host.name = self.addHost.name.text()
        host.ram = int(self.addHost.ram.text())
        host.cpu_infos = []
        host.video_card_infos = []
        gpus = []
        for i in range(len(self.addHost.cpu_cores_edits)):
            host.cpu_infos.append(CPUInfo(int(self.addHost.cpu_cores_edits[i].text()), int(self.addHost.cpu_flops_edits[i].text())))
        for i in range(len(self.addHost.gpu_cores_edits)):
            gpu = GPUInfo()
            gpu.cores = int(self.addHost.gpu_cores_edits[i].text())
            gpu.core_per_sm = int(self.addHost.gpu_sm_edits[i].text())
            gpu.max_block_per_sm = int(self.addHost.gpu_max_block_edits[i].text())
            gpu.flops_per_core = int(self.addHost.gpu_flops_edits[i].text())
            gpu.gddram = int(self.addHost.gpu_mem_edits[i].text())
            gpus.append(gpu)
        if len(gpus) > 0:
            host.video_card_infos.append(VideoCardInfo(gpus))
            host.video_card_infos[0].pcie_bw = int(self.addHost.pcie.text())
        self.jobSim.bindHostInfo(self.item, host)
        self.hide()
        self.addHost.hide()

    def setColumnWidthAsProportion(self, table: QTableWidget,proportionList, width):
        for i, proportion in enumerate(proportionList):
            wid = width * proportion / sum(proportionList)
            table.setColumnWidth(i, int(wid))

    def setRowHeightAsNum(self, table: QTableWidget,height: int):
        for i in range(table.rowCount()):
            table.setRowHeight(i, int(height / table.rowCount()))

    def setFontOfTable(self, table: QTableWidget):
        font = QFont()
        font.setPointSize(20)
        table.setFont(font)
        table.horizontalHeader().setFont(font)