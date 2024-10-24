from util.jobSim import GPUInfo, CPUInfo
# 这里设置了一些固定的类型，包括显卡和CPU

class GPU:
    def __init__(self, name, gddram, flops, cores, sms):
        self.name = name
        self.gddram = gddram
        self.flops = flops
        self.core_num = cores
        self.sm_num = sms

    def getGPUInfo(self):
        return GPUInfo(self.core_num, (int)(self.core_num / self.sm_num), 24, self.gddram, self.flops)

def getNVIDIA4060():
    return GPU("NVIDIA RTX 4060", 8, 22, 3072, 24)

def getNVIDIA4080():
    return GPU("NVIDIA RTX 4080", 12, 30, 6144, 48)

def getNVIDIA4090():
    return GPU("NVIDIA RTX 4090", 24, 35, 8192, 64)

def getNVIDIA3060():
    return GPU("NVIDIA RTX 3060", 12, 12, 3584, 28)

class CPU:
    def __init__(self, name, cores, threads, flops):
        self.name = name
        self.core_num = cores
        self.flops = flops

    def getCPUInfo(self):
        return CPUInfo(self.core_num, self.flops)

def getIntelI710700():
    return CPU("Intel i7-10700", 8, 16, 16)