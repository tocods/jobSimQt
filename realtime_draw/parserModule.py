import os
import re


class ParserModule:
    def __init__(self, path):
        self.reopen(path)

    def reopen(self, path):
        self.path = path
        self.reload()

    def reload(self):
        with open(
            os.path.join(self.path, "Parameters.ini"), "r"
        ) as file:
            configText = file.read()
            flowNameList = re.findall(r'\bflowName\s*=\s*"([^"]+)"', configText)
        self.flowNameList = flowNameList
        self.flowNameLossList = []
        for name in self.flowNameList:
            self.flowNameLossList.append(name + "_loss")
        self.reset()

    def reset(self):
        self.latencyVectorList = []
        self.bufferVectorList = []
        self.lossVectorList = []
        self.flowNameVector = {}
        self.hostNameVector = {}
        self.flowNameLossVector = {}
        self.latencyResultX = {}
        self.latencyResultY = {}
        self.latencyResultMaxX = {}
        self.latencyResultMaxY = {}
        self.maxLatency = 0.0
        self.bufferResultX = {}
        self.bufferResultY = {}
        self.bufferResultMaxX = {}
        self.bufferResultMaxY = {}
        self.maxBuffer = 0.0

        self.lossResult = {}

    def loadVectorConfigLine(self, line):
        strlist = line.split(" ")
        if strlist[0] == "vector":
            id = int(strlist[1])
            if strlist[3] in self.flowNameList:
                self.latencyVectorList.append(id)
                self.flowNameVector[strlist[3]] = id
                self.latencyResultX[id] = []
                self.latencyResultY[id] = []
                self.latencyResultMaxX[id] = 0.0
                self.latencyResultMaxY[id] = 0.0
            if strlist[3][:4] == "615.":
                self.bufferVectorList.append(id)
                host_name = strlist[3].split(".")[1]
                self.hostNameVector[host_name] = id
                self.bufferResultX[id] = []
                self.bufferResultY[id] = []
                self.bufferResultMaxX[id] = 0.0
                self.bufferResultMaxY[id] = 0.0
            if strlist[3] in self.flowNameLossList:
                self.lossVectorList.append(id)
                self.flowNameLossVector[strlist[3]] = id
                self.lossResult[id] = 0.0
                

    def loadDataLine(self, line):
        line_list = line.strip("\n").split("\t")
        if len(line_list) != 4:
            return
        id = int(line_list[0])
        if id in self.latencyVectorList:
            self.latencyResultX[id].append(float(line_list[2]) * 1000)
            self.latencyResultY[id].append(float(line_list[3]) * 1000)
            self.latencyResultMaxX[id] = max(
                self.latencyResultMaxX[id], float(line_list[2]) * 1000
            )
            self.latencyResultMaxY[id] = max(
                self.latencyResultMaxY[id], float(line_list[3]) * 1000
            )
        elif id in self.bufferVectorList:
            self.bufferResultX[id].append(float(line_list[2]))
            self.bufferResultY[id].append(float(line_list[3]))
            self.bufferResultMaxX[id] = max(
                self.bufferResultMaxX[id], float(line_list[2])
            )
            self.bufferResultMaxY[id] = max(
                self.bufferResultMaxY[id], float(line_list[3])
            )
        elif id in self.lossVectorList:
            self.lossResult[id] = max(self.lossResult[id], float(line_list[3]))


    def loadData(self):
        self.reload()
        resultPath = os.path.join(self.path, "results", "General-#0.vec")
        with open(resultPath, "r") as fp:
        # with open(resultPath, "r", encoding="utf-8") as fp:
            for line in fp:
                if line == "":
                    continue
                if not line[0].isdigit():
                    self.loadVectorConfigLine(line)
                else:
                    self.loadDataLine(line)
