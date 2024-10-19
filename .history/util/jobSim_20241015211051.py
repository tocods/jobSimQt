from typing import List, Optional
from terminaltables import AsciiTable
import xml.etree.ElementTree as ET
import json

class CPUInfo:
    def __init__(self, cores: Optional[int] = None, mips: Optional[float] = None):
        self.cores = cores
        self.mips = mips

class GPUInfo:
    def __init__(self, cores: Optional[int] = None, core_per_sm: Optional[int] = None, max_block_per_sm: Optional[int] = None, gddram: Optional[int] = None, flops_per_core: Optional[float] = None):
        self.cores = cores
        self.core_per_sm = core_per_sm
        self.max_block_per_sm = max_block_per_sm
        self.gddram = gddram
        self.flops_per_core = flops_per_core

class VideoCardInfo:
    def __init__(self, gpu_infos: Optional[List[GPUInfo]] = None):
        self.gpu_infos = gpu_infos
        self.pcie_bw = 0

    def get_gpu_infos(self) -> List[GPUInfo]:
        return self.gpu_infos

class HostInfo:
    def __init__(self, name: Optional[str] = None, video_card_infos: Optional[List[VideoCardInfo]] = None, cpu_infos: Optional[List[CPUInfo]] = None, ram: Optional[int] = None):
        self.name = name
        self.video_card_infos = video_card_infos
        self.cpu_infos = cpu_infos
        self.ram = ram


    def print(self) -> str:
        table_data = [
            ["Name", "FaultGenerator", "Scale", "Shape", "", ""]
        ]

        table_data.append([self.name,"", "", "", "", ""])

        table_data.append(["CPU", "cores", "mips", "", "", ""])
        for i, cpu_info in enumerate(self.cpu_infos):
            table_data.append([i, cpu_info.cores, cpu_info.mips, "", "", ""])

        if self.video_card_infos:
            table_data.append(["GPU", "cores", "coresPerSM", "maxBlockPerSM", "Gddram", "FLOPS"])
            for i, video_card_info in enumerate(self.video_card_infos):
                for gpu_info in video_card_info.get_gpu_infos():
                    table_data.append([i, gpu_info.cores, gpu_info.core_per_sm, gpu_info.max_block_per_sm, gpu_info.gddram, gpu_info.flops_per_core])

        table = AsciiTable(table_data)
        table.inner_row_border = True
        print(table.table)
        return table.table
    
class CPUTaskInfo:
    def __init__(self, ram: Optional[int] = None, pes_number: Optional[int] = None, length: Optional[float] = None):
        self.ram = ram
        self.pes_number = pes_number
        self.length = length

class GPUTaskInfo:
    class Kernel:
        def __init__(self, block_num: Optional[int] = None, thread_num: Optional[int] = None, flops: Optional[float] = None):
            self.block_num = block_num
            self.thread_num = thread_num
            self.thread_length = flops

    def __init__(self, kernels: Optional[List['GPUTaskInfo.Kernel']] = None, requested_gddram_size: Optional[int] = None, task_input_size: Optional[int] = None, task_output_size: Optional[int] = None):
        self.kernels = kernels
        self.requested_gddram_size = requested_gddram_size
        self.task_input_size = task_input_size
        self.task_output_size = task_output_size

class TaskInfo:
    def __init__(self, cpu_task_info: Optional[CPUTaskInfo] = None, gpu_task_info: Optional[GPUTaskInfo] = None):
        self.cpu_task_info = cpu_task_info
        self.gpu_task_info = gpu_task_info

class JobInfo:
    def __init__(self, name: Optional[str] = None, period: Optional[float] = None, cpu_task: Optional[CPUTaskInfo] = None, gpu_task: Optional[GPUTaskInfo] = None):
        self.name = name
        self.period = period
        self.cpu_task = cpu_task
        self.gpu_task = gpu_task
        

    def print(self) -> str:
        table_data = [
            ["name", "period", "memory", ""],
            [self.name, self.period, self.cpu_task.ram, ""]
        ]

        table_data.append(["Device", "cores", "mi", ""])
        table_data.append(["CPU", self.cpu_task.pes_number, self.cpu_task.length, ""])
        if self.gpu_task is not None:
            print("1 is not NONE")
        if self.gpu_task is not None and self.gpu_task is not None:
            print("2 is not NONE")
        if self.gpu_task is not None and self.gpu_task is not None and self.gpu_task.kernels:
            table_data.append(["Kernel", "blockNum", "threadPerBlock", "FLOP"])
            for i, kernel in enumerate(self.gpu_task.kernels):
                table_data.append([i, kernel.block_num, kernel.block_num, kernel.thread_length])

        table = AsciiTable(table_data)
        table.inner_row_border = True
        table.justify_columns = {i: 'center' for i in range(len(table_data[0]))}
        print(table.table)
        return table.table
    
class FaultGenerator:
    def __init__(self, type, scale: Optional[float]=None, shape: Optional[float]=None):
        self.mttf_type = type
        self.mttf_scale = scale
        self.mttf_shape = shape
        self.mttf_type = type
        self.mttf_scale = scale
        self.mttf_shape = shape

    def setAim(self, aim):
        self.aim = aim

    def print(self) -> str:
        table_data = [
            ["mttf_type", "mttf_scale", "mttf_shape", "mttr_type", "mttr_scale", "mttr_shape"],
            [self.mttf_type, self.mttf_scale, self.mttf_shape, self.mttr_type, self.mttr_scale, self.mttr_shape]
        ]

        table = AsciiTable(table_data)
        table.inner_row_border = True
        table.justify_columns = {i: 'center' for i in range(len(table_data[0]))}
        print(table.table)
        return table.table

   
class ParseUtil:
    def __init__(self):
        self.host_infos = []
        self.job_infos = []
        self.fault_infos = []
        self.duration = 0.0


    def get_host_infos(self):
        return self.host_infos

    def get_job_infos(self):
        return self.job_infos
    
    def get_fault_infos(self):
        return self.fault_infos

    def parse_gpu_info(self, gpu):
        gpu_info = GPUInfo()
        for property in gpu:
            if property.tag == "memory":
                gpu_info.gddram = int(property.text)
            elif property.tag == "cores":
                gpu_info.cores = int(property.text)
            elif property.tag == "coresPerSM":
                gpu_info.core_per_sm = int(property.text)
            elif property.tag == "flops":
                gpu_info.flops_per_core = int(property.text)
            elif property.tag == "maxBlockNum":
                gpu_info.max_block_per_sm = int(property.text)
        return gpu_info

    def parse_video_card_info(self, video_card):
        video_card_info = VideoCardInfo()
        video_card_info.gpu_infos = []
        for property in video_card:
            if property.tag == "name":
                video_card_info.name = property.text
            elif property.tag == "pcieBandwidth":
                video_card_info.pcie_bw = int(property.text)
            elif property.tag == "gpus":
                num = int(property.attrib["num"])
                for _ in range(num):
                    video_card_info.gpu_infos.append(self.parse_gpu_info(property))
        return video_card_info

    def parse_cpu_info(self, cpu):
        cpu_info = CPUInfo()
        for property in cpu:
            if property.tag == "name":
                cpu_info.name = property.text
            elif property.tag == "cores":
                cpu_info.cores = int(property.text)
            elif property.tag == "flops":
                cpu_info.mips = int(property.text)
        return cpu_info

    def parse_ram_info(self, ram):
        for property in ram:
            if property.tag == "size":
                return int(property.text)
        return -1

    def parse_fault_generator(self, generator):
        type = generator.attrib.get("type", "")
        scale = float('inf')
        shape = float('inf')
        for property in generator:
            if property.tag == "scale":
                scale = float(property.text)
            elif property.tag == "shape":
                shape = float(property.text)
        if shape == float('inf') or scale == float('inf'):
            return None
        ret = FaultGenerator(type, scale, shape)
        return ret
    
    def parse_fault_xml(self, file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            for fault in root:
                if fault.tag != "faultInjection":
                    print(f"标签为{fault.tag}项，应为faultInjection")
                    continue
                fault_inject = FaultGenerator()
                fault_inject.type = fault.attrib.get("type", "")
                fault_inject.scale = float('inf')
                fault_inject.shape = float('inf')
                for property in fault:
                    if property.tag == "scale":
                        fault_inject.scale = float(property.text)
                    elif property.tag == "shape":
                        fault_inject.shape = float(property.text)
                    else:
                        print(f"包含无法解析的字段：{property.tag}")
                if fault_inject.shape == float('inf') or fault_inject.scale == float('inf'):
                    continue
                self.fault_infos.append(fault_inject)
            return None
        except Exception as e:
            print(e)
            return None

    def parse_host_xml(self, file_path):
        try:
            ret = []
            tree = ET.parse(file_path)
            root = tree.getroot()
            for host in root:
                if host.tag != "host":
                    print(f"标签为{host.tag}项，应为host")
                    continue
                host_info = HostInfo()
                host_info.name = host.attrib["name"]
                host_info.cpu_infos = []
                host_info.video_card_infos = []
                for property in host:
                    if property.tag == "videoCard":
                        host_info.video_card_infos.append(self.parse_video_card_info(property))
                    elif property.tag == "cpus":
                        num = int(property.attrib["num"])
                        for _ in range(num):
                            host_info.cpu_infos.append(self.parse_cpu_info(property))
                    elif property.tag == "memory":
                        host_info.ram = self.parse_ram_info(property)
                    elif property.tag == "faultInjection":
                        host_info.generator = self.parse_fault_generator(property)
                    else:
                        print(f"包含无法解析的字段：{property.tag}")
                #ret.append(host_info.print())
                self.host_infos.append(host_info)
            return "\n".join(ret)
        except Exception as e:
            print(e)
            return ""

    def parse_cpu_task_info(self, cpu_task):
        cpu_task_info = CPUTaskInfo()
        for property in cpu_task:
            if property.tag == "cores":
                cpu_task_info.pes_number = int(property.text)
            elif property.tag == "flop":
                cpu_task_info.length = int(property.text)
        cpu_task_info.file_size = 0
        cpu_task_info.output_size = 0
        return cpu_task_info

    def parse_gpu_task_info(self, gpu_task):
        gpu_task_info = GPUTaskInfo()
        gpu_task_info.kernels = []
        for property in gpu_task:
            if property.tag == "memory":
                gpu_task_info.requested_gddram_size = int(property.text)
            elif property.tag == "inputSize":
                gpu_task_info.task_input_size = int(property.text)
            elif property.tag == "outputSize":
                gpu_task_info.task_output_size = int(property.text)
            elif property.tag == "kernels":
                for kernel in property:
                    if kernel.tag != "kernel":
                        continue
                    block_num = 0
                    thread_num = 0
                    flop = 0
                    for block_property in kernel:
                        if block_property.tag == "blockNum":
                            block_num = int(block_property.text)
                        elif block_property.tag == "threadNum":
                            thread_num = int(block_property.text)
                        elif block_property.tag == "flop":
                            flop = int(block_property.text)
                    kernel_info = GPUTaskInfo.Kernel()
                    kernel_info.block_num = block_num
                    kernel_info.thread_length = flop
                    kernel_info.thread_num = thread_num
                    gpu_task_info.kernels.append(kernel_info)
        return gpu_task_info

    def parse_job_xml(self, file_path):
        try:
            ret = []
            tree = ET.parse(file_path)
            root = tree.getroot()
            for job in root:
                if job.tag not in ["job", "duration"]:
                    print(f"标签为{job.tag}项，应为job / duration")
                    continue
                if job.tag == "duration":
                    self.duration = float(job.text)
                    continue
                job_info = JobInfo()
                memory = 0.0
                job_info.period = float(job.attrib.get("period", 0))
                job_info.name = job.attrib["name"]
                for property in job:
                    if property.tag == "cpu":
                        task_info = TaskInfo()
                        task_info.cpu_task_info = self.parse_cpu_task_info(property)
                        task_info.gpu_task_info = None
                        job_info.cpu_task = task_info
                    elif property.tag == "gpu":
                        task_info = TaskInfo()
                        task_info.cpu_task_info = None
                        task_info.gpu_task_info = self.parse_gpu_task_info(property)
                        job_info.gpu_task = task_info
                    elif property.tag == "memory":
                        memory = float(property[0].text)
                    elif property.tag == "faultInjection":
                        job_info.generator = self.parse_fault_generator(property)
                    else:
                        print(f"包含无法解析的字段：{property.tag}")
                job_info.cpu_task.cpu_task_info.ram = memory
                #ret.append(job_info.print())
                self.job_infos.append(job_info)
            return "\n".join(ret)
        except Exception as e:
            print(e)
            return ""
        
    def parseHosts(self, path):
        json_file = open(path, "r")
        json_data = json.load(json_file)
        json_file.close()
        hosts = []
        for host in json_data:
            host_info = HostInfo()
            host_info.name = host["name"]
            host_info.cpu_infos = []
            for cpu in host["cpu_infos"]:
                cpu_info = CPUInfo()
                cpu_info.cores = cpu["cores"]
                cpu_info.mips = cpu["mips"]
                host_info.cpu_infos.append(cpu_info)
            host_info.ram = host["ram"]
            host_info.video_card_infos = []
            for video_card in host["video_card_infos"]:
                video_card_info = VideoCardInfo()
                video_card_info.gpu_infos = []
                for gpu in video_card["gpus"]:
                    gpu_info = GPUInfo()
                    gpu_info.cores = gpu["cores"]
                    gpu_info.core_per_sm = gpu["core_per_sm"]
                    gpu_info.max_block_per_sm = gpu["max_block_per_sm"]
                    gpu_info.gddram = gpu["gddram"]
                    gpu_info.flops_per_core = gpu["flops_per_core"]
                    video_card_info.gpu_infos.append(gpu_info)
                video_card_info.pcie_bw = video_card["pcie_bw"]
                host_info.video_card_infos.append(video_card_info)
            hosts.append(host_info)
        return hosts
    
    def parseJobs(self, path):
        json_file = open(path, "r")
        json_data = json.load(json_file)
        json_file.close()
        jobs = []
        for job in json_data:
            job_info = JobInfo()
            job_info.name = job["name"]
            job_info.period = job["period"]
            cpu_task = CPUTaskInfo()
            cpu_task.ram = job["cpu_task"]["ram"]
            cpu_task.pes_number = job["cpu_task"]["pes_number"]
            cpu_task.length = job["cpu_task"]["length"]
            job_info.cpu_task = cpu_task
            gpu_task = GPUTaskInfo()
            gpu_task.requested_gddram_size = job["gpu_task"]["requested_gddram_size"]
            gpu_task.task_input_size = job["gpu_task"]["task_input_size"]
            gpu_task.task_output_size = job["gpu_task"]["task_output_size"]
            gpu_task.kernels = []
            for kernel in job["gpu_task"]["kernels"]:
                kernel_info = GPUTaskInfo.Kernel()
                kernel_info.block_num = kernel["block_num"]
                kernel_info.thread_num = kernel["thread_num"]
                kernel_info.thread_length = kernel["thread_length"]
                gpu_task.kernels.append(kernel_info)
            job_info.gpu_task = gpu_task
            jobs.append(job_info)
        return jobs
    
    def parseFaults(self, path):
        json_file = open(path, "r")
        json_data = json.load(json_file)
        json_file.close()
        faults = []
        for fault in json_data:
            fault_info = FaultGenerator()
            scale = fault["mttf_scale"]
            shape = fault["mttf_shape"]
            ttype = fault["mttf_type"]
            fault_info = FaultGenerator()
            faults.append(fault_info)
        return faults


class jobSim:
    def __init__(self):
        self.parse_util = ParseUtil()
        self.hosts = {}
        self.onlyCPU = {}
        self.jobs = []
        self.faults = []
        self.duration = -1
        self.scheduler = 0
 
    def addJob(self, job_info: JobInfo):
        self.jobs.append(job_info)
    
    def addFault(self, fault_info: FaultGenerator):
        self.faults.append(fault_info)


global sysSim
sysSim = jobSim()