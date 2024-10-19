import matplotlib.pyplot as plt
import matplotlib as mat
import numpy as np
import xml.etree.ElementTree as ET
from terminaltables import AsciiTable
from PySide6.QtCharts import QChart,QChartView,QLineSeries,QDateTimeAxis,QValueAxis

class KernelRecord:
    def __init__(self, id, h2d, d2h, start, end, duration):
        self.id = id
        self.h2d = h2d
        self.d2h = d2h
        self.start = start
        self.end = end
        self.duration = duration

class JobRun:
    def __init__(self, status, host, start, end, duration):
        self.status = status
        self.host = host
        self.start = start
        self.end = end
        self.duration = duration
        self.kernelRecords = []

    def addKernelRecord(self, kernelRecord):
        self.kernelRecords.append(kernelRecord)

class JobRecord:
    def __init__(self, jobName):
        self.jobName = jobName
        self.jobRuns = []

    def addJobRun(self, jobRun):
        self.jobRuns.append(jobRun)

    def getJobRun(self, index):
        return self.jobRuns[index]
    
    def print(self):
        table_data = [
            ['Job Name', self.jobName],
            ['Status', 'Host', 'Start', 'End', 'Duration']
        ]
        for jobRun in self.jobRuns:
            table_data.append([jobRun.status, jobRun.host, jobRun.start, jobRun.end, jobRun.duration])
            table_data.append(['Kernel ID', 'H2D', 'D2H', 'Start', 'End', 'Duration'])
            for kernelRecord in jobRun.kernelRecords:
                table_data.append([kernelRecord.id, kernelRecord.h2d, kernelRecord.d2h, kernelRecord.start, kernelRecord.end, kernelRecord.duration])
        table = AsciiTable(table_data)
        print(table.table)
    

class FaultRecord:
    def __init__(self, time, object, isFalseAlarm, type, isSuccessRebuild, redundancyBefore, redundancyAfter):
        self.time = time
        self.object = object
        self.isFalseAlarm = isFalseAlarm
        self.type = '主机宕机' if type == 'rebuild' else '任务超时'
        self.isSuccessRebuild = isSuccessRebuild
        self.redundancyBefore = redundancyBefore
        self.redundancyAfter = redundancyAfter
    
    def print(self):
        table_data = [
            ['Time', self.time],
            ['Object', self.object],
            ['Is False Alarm', self.isFalseAlarm]
        ]
        table = AsciiTable(table_data)
        print(table.table)

class GpuUtilization:
    def __init__(self, gpu, time, utilization):
        self.gpu = gpu
        self.time = time
        self.utilization = utilization

class HostUtilization:
    def __init__(self, host, time, cpuUtilization, ramUtilization):
        self.host = host
        self.time = time
        self.cpuUtilization = cpuUtilization
        self.ramUtilization = ramUtilization
        self.gpuUtilizations = []

    def addGPUUtilization(self, gpuUtilization):
        self.gpuUtilizations.append(gpuUtilization)

class HostRecord:
    def __init__(self, hostName):
        self.hostName = hostName
        self.hostUtilizations = []
        self.avgCpuUtilization = 0
        self.avgRamUtilization = 0
        self.avgGpuUtilization = 0
        self.maxCpuUtilization = 0
        self.maxRamUtilization = 0
        self.maxGpuUtilization = 0
    
    def calculateUtilization(self):
        cpuUtilizationList = self.getCpuUilizationList()
        ramUtilizationList = self.getRamUilizationList()
        gpuUtilizationList = self.getGpuUilizationList('0')
        if len(cpuUtilizationList) != 0:
            maxV = -1
            avg = 0
            for hostUtilization in self.hostUtilizations:
                avg += float(hostUtilization.cpuUtilization)
                if float(hostUtilization.cpuUtilization) > maxV:
                    maxV = float(hostUtilization.cpuUtilization)
            self.avgCpuUtilization = avg / len(cpuUtilizationList)
            self.maxCpuUtilization = maxV
        if len(ramUtilizationList) != 0:
            maxV = -1
            avg = 0
            for hostUtilization in self.hostUtilizations:
                avg += float(hostUtilization.ramUtilization)
                if float(hostUtilization.ramUtilization) > maxV:
                    maxV = float(hostUtilization.ramUtilization)
            self.avgRamUtilization = avg / len(ramUtilizationList)
            self.maxRamUtilization = maxV
        if len(gpuUtilizationList) != 0:
            maxV = -1
            avg = 0
            for hostUtilization in self.hostUtilizations:
                for gpuUtilization in hostUtilization.gpuUtilizations:
                    avg += float(gpuUtilization.utilization)
                    if float(gpuUtilization.utilization) > maxV:
                        maxV = float(gpuUtilization.utilization)
            self.avgGpuUtilization = avg / len(gpuUtilizationList)
            self.maxGpuUtilization = maxV

    def addHostUtilization(self, hostUtilization):
        self.hostUtilizations.append(hostUtilization)

    def getHostUtilization(self, index):
        return self.hostUtilizations[index]
    
    def getHostUtilizationByTime(self, time):
        for hostUtilization in self.hostUtilizations:
            if hostUtilization.time == time:
                return hostUtilization
        return None
    
    def getHostUtilizationByTimeRange(self, startTime, endTime):
        hostUtilizations = []
        for hostUtilization in self.hostUtilizations:
            if float(hostUtilization.time) >= startTime and float(hostUtilization.time) <= endTime:
                hostUtilizations.append(hostUtilization)
        return hostUtilizations
    
    def getCpuUilizationList(self):
        cpuUtilizationList = []
        for hostUtilization in self.hostUtilizations:
            cpuUtilizationList.append(hostUtilization.cpuUtilization)
        return cpuUtilizationList
    
    def getRamUilizationList(self):
        ramUtilizationList = []
        for hostUtilization in self.hostUtilizations:
            ramUtilizationList.append(hostUtilization.ramUtilization)
        return ramUtilizationList
    
    def getGpuUilizationList(self, gpu):
        gpuUtilizationList = []
        for hostUtilization in self.hostUtilizations:
            for gpuUtilization in hostUtilization.gpuUtilizations:
                if gpuUtilization.gpu == gpu:
                    gpuUtilizationList.append(gpuUtilization.utilization)
        return gpuUtilizationList
    
    def getGpuUilizationListByTimeRange(self, gpu, startTime, endTime):
        gpuUtilizationList = []
        for hostUtilization in self.hostUtilizations:
            if float(hostUtilization.time) >= startTime and float(hostUtilization.time) <= endTime:
                for gpuUtilization in hostUtilization.gpuUtilizations:
                    if gpuUtilization.gpu == gpu:
                        gpuUtilizationList.append(gpuUtilization.utilization)
        return gpuUtilizationList
    
    def print(self):
        table_data = [
            ['Host Name', self.hostName],
            ['Time', 'CPU Utilization', 'RAM Utilization']
        ]
        for hostUtilization in self.hostUtilizations:
            table_data.append([hostUtilization.time, hostUtilization.cpuUtilization, hostUtilization.ramUtilization])
            table_data.append(['GPU', 'Time', 'Utilization'])
            for gpuUtilization in hostUtilization.gpuUtilizations:
                table_data.append([gpuUtilization.gpu, gpuUtilization.time, gpuUtilization.utilization])
        table = AsciiTable(table_data)
        print(table.table)
    
class ClusterRecord:
    def __init__(self):
        self.hostRecords = []

    def addHostRecord(self, hostRecord):
        self.hostRecords.append(hostRecord)

    def print(self):
        for hostRecord in self.hostRecords:
            hostRecord.print()

class XmlParser:
    def __init__(self, file):
        self.file = file
        self.tree = ET.parse(file)
        self.root = self.tree.getroot()

    def parseJobRecord(self):
        jobRecordList = []
        for jobRecordElement in self.root.findall('Job'):
            jobRecord = JobRecord(jobRecordElement.attrib['name'])
            for jobRunElement in jobRecordElement.findall('RunningRecord'):
                jobRun = JobRun(jobRunElement.attrib['status'], jobRunElement.attrib['host'], jobRunElement.attrib['start'], jobRunElement.attrib['end'], jobRunElement.attrib['duration'])
                for kernelRecordElement in jobRunElement.findall('KernelRecord'):
                    kernelRecord = KernelRecord(kernelRecordElement.attrib['id'], kernelRecordElement.attrib['h2d'], kernelRecordElement.attrib['d2h'], kernelRecordElement.attrib['start'], kernelRecordElement.attrib['end'], kernelRecordElement.attrib['duration'])
                    jobRun.addKernelRecord(kernelRecord)
                jobRecord.addJobRun(jobRun)
            jobRecordList.append(jobRecord)
        return jobRecordList
    
    def parseFaultRecord(self):
        faultRecordList = []
        for faultRecordElement in self.root.findall('faultRecord'):
            faultRecord = FaultRecord(faultRecordElement.attrib['time'], faultRecordElement.attrib['object'], faultRecordElement.attrib['isFalseAlarm'],
                                      faultRecordElement.attrib['type'], faultRecordElement.attrib['isSuccessRebuild'], faultRecordElement.attrib['redundancyBefore'], faultRecordElement.attrib['redundancyAfter'])
            faultRecordList.append(faultRecord)
        return faultRecordList
    
    def parseHostRecord(self):
        clusterRecord = ClusterRecord()
        hostRecords = {}
        for utilRecordElement in self.root.findall('Util'):
            time = utilRecordElement.attrib['time']
            for hostRecordElement in utilRecordElement.findall('Host'):
                name = hostRecordElement.attrib['name']
                hostUtilization = HostUtilization(name, time, hostRecordElement.attrib['cpuUtilization'], hostRecordElement.attrib['ramUtilization'])
                for gpuUtilElement in hostRecordElement.findall('gpuUtilization'):
                    gpuUtilization = GpuUtilization(gpuUtilElement.attrib['id'], time, gpuUtilElement.attrib['gpu'])
                    hostUtilization.addGPUUtilization(gpuUtilization)
                if name in hostRecords:
                    hostRecords[name].addHostUtilization(hostUtilization)
                else:
                    hostRecord = HostRecord(name)
                    hostRecord.addHostUtilization(hostUtilization)
                    hostRecords[name] = hostRecord
        for hostRecord in hostRecords.values():
            clusterRecord.addHostRecord(hostRecord)
        return clusterRecord
    
class Painter():
    def __init__(self, clusterRecord, jobRecords, faultRecords):
        self.clusterRecord = clusterRecord
        self.jobRecords = jobRecords
        self.faultRecords = faultRecords
        mat.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）


    '''
    Plot CPU utilization of the cluster

    hostName: name of the host
    startTime: start time of the plot
    endTime: end time of the plot
    '''
    def plotHostUtilization(self, hostName, startTime, endTime):
        chart = QChart()
        seriesCPU = QLineSeries()
        seriesRam = QLineSeries()

        hostRecord = self.clusterRecord.hostRecords[0]
        for h in self.clusterRecord.hostRecords:
            if h.hostName == hostName:
                hostRecord = h
                break
        hostUtilizations = hostRecord.getHostUtilizationByTimeRange(startTime, endTime)
        timeList = []
        cpuUtilizationList = []
        ramUtilizationList = []
        for hostUtilization in hostUtilizations:
            timeList.append(float(hostUtilization.time))
            cpuUtilizationList.append(float(hostUtilization.cpuUtilization))
            ramUtilizationList.append(float(hostUtilization.ramUtilization))
            
        plt.plot(timeList, cpuUtilizationList, label='CPU利用率')
        plt.plot(timeList, ramUtilizationList, label='内存利用率')
        plt.xlabel('时间')
        plt.ylabel('利用率')
        plt.title(hostName + '利用率')
        plt.legend()
        plt.show()

    def plotHostCPUUtilization(self, hostName, startTime, endTime):
        hostRecord = self.clusterRecord.hostRecords[0]
        for h in self.clusterRecord.hostRecords:
            if h.hostName == hostName:
                hostRecord = h
                break
        hostUtilizations = hostRecord.getHostUtilizationByTimeRange(startTime, endTime)
        timeList = []
        cpuUtilizationList = []
        for hostUtilization in hostUtilizations:
            timeList.append(float(hostUtilization.time))
            cpuUtilizationList.append(float(hostUtilization.cpuUtilization))
        plt.plot(timeList, cpuUtilizationList, label='CPU利用率')
        plt.xlabel('时间')
        plt.ylabel('利用率')
        plt.title('CPU利用率')
        plt.legend()
        plt.show()

    def plotHostRamUtilization(self, hostName, startTime, endTime):
        hostRecord = self.clusterRecord.hostRecords[0]
        for h in self.clusterRecord.hostRecords:
            if h.hostName == hostName:
                hostRecord = h
                break
        hostUtilizations = hostRecord.getHostUtilizationByTimeRange(startTime, endTime)
        timeList = []
        ramUtilizationList = []
        for hostUtilization in hostUtilizations:
            timeList.append(float(hostUtilization.time))
            ramUtilizationList.append(float(hostUtilization.ramUtilization))
        plt.plot(timeList, ramUtilizationList, label='内存利用率')
        plt.xlabel('时间')
        plt.ylabel('利用率')
        plt.title('内存利用率')
        plt.legend()
        plt.show()

    '''
    Plot GPU utilization of a host

    hostName: name of the host
    gpu: id of the gpu
    startTime: start time of the plot
    endTime: end time of the plot
    '''
    def plotGpuUtilization(self, hostName, gpu, startTime, endTime):
        hostRecord = self.clusterRecord.hostRecords[0]
        for h in self.clusterRecord.hostRecords:
            if h.hostName == hostName:
                hostRecord = h
                break
        if gpu != -1:
            gpuUtilizationList = hostRecord.getGpuUilizationListByTimeRange(gpu, startTime, endTime)
            timeList = []
            for hostUtilization in hostRecord.hostUtilizations:
                if float(hostUtilization.time) >= startTime and float(hostUtilization.time) <= endTime:
                    timeList.append(hostUtilization.time)
            if len(gpuUtilizationList) == 0:
                print('No GPU utilization record found')
                # QMessageBox.information(self, '', '主机不包含GPU')
                return
            plt.plot(timeList, gpuUtilizationList, label='GPU Utilization')
            plt.xlabel('Time')
            plt.ylabel('Utilization')
            plt.title('GPU Utilization')
            plt.legend()
            plt.show()
        else:
            gpus = len(hostRecord.hostUtilizations[0].gpuUtilizations)
            if gpus == 0:
                print('No GPU utilization record found')
                #QMessageBox.information(self, '', '主机不包含GPU')
                return
            for i in range(gpus):
                gpuUtilizationList = hostRecord.getGpuUilizationListByTimeRange(str(i), startTime, endTime)
                timeList = []
                for hostUtilization in hostRecord.hostUtilizations:
                    if float(hostUtilization.time) >= startTime and float(hostUtilization.time) <= endTime:
                        timeList.append(hostUtilization.time)
                label = 'GPU ' + str(i) + ' 利用率'
                plt.plot(timeList, gpuUtilizationList, label=label)
            plt.xlabel('时间')
            plt.ylabel('利用率')
            plt.title('GPU利用率')
            plt.legend()
            plt.show()

    def plotJobDuration(self, jobName):
        for jobRecord in self.jobRecords:
            print(jobRecord.jobName)
            print(len(jobRecord.jobRuns))
            if jobRecord.jobName == jobName:
                timeList = []
                durationList = []
                for jobRun in jobRecord.jobRuns:
                    timeList.append(float(jobRun.start))
                    durationList.append(float(jobRun.duration))
                #每个柱子顶上显示数值
                i = 0
                for a, b in zip(timeList, durationList):
                    plt.text(i, a+b, '%.0f' % b, ha='center', va='bottom', fontsize=10)
                    i += 1
                plt.grid(ls="--", alpha=0.5)
                plt.bar(np.arange(len(jobRecord.jobRuns)), durationList, bottom=timeList, label='Duration')
                plt.xlabel('周期')
                plt.ylabel('时间')
                plt.title(jobName + '运行时间')
                plt.legend()
                plt.show()

    def plotFaultRecord(self):
        timeList = []
        faultList = []
        for faultRecord in self.faultRecords:
            timeList.append(float(faultRecord.time))
            faultList.append(1 if faultRecord.isFalseAlarm == 'true' else 0)
        plt.plot(timeList, faultList, label='Fault')
        plt.xlabel('Time')
        plt.ylabel('Fault')
        plt.title('Fault Record')
        plt.legend()
        plt.show()

# xmlParser = XmlParser('OutputFiles/jobRun.xml')
# jobRecords = xmlParser.parseJobRecord()
# painter = Painter([], jobRecords, [])
# painter.plotJobDuration('j')
# xmlParser = XmlParser('OutputFiles/faultRecords.xml')
# faultRecords = xmlParser.parseFaultRecord()
# xmlParser = XmlParser('OutputFiles/hostUtils.xml')
# clusterRecord = xmlParser.parseHostRecord()
# painter = Painter(clusterRecord, jobRecords, faultRecords)
# painter.plotHostUtilization('host2', 0, 10)
# painter.plotGpuUtilization('host1', '0', 0, 10)