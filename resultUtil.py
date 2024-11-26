from jobSimPainter import HostRecord, HostUtilization, JobRecord, JobRun, FaultRecord, ClusterRecord
from util.jobSim import JobInfo, sysSim
from typing import List
# 为了对比异构计算夏不同计算单元构成时的性能，我们需要对不同计算单元的性能进行比较

# 计算一个任务的平均运行时间
def getAverageRunTime(job: JobRecord):
    time_total = 0.0
    for jobRun in job.jobRuns:
        time_total += (float)(jobRun.duration)
    return time_total / len(job.jobRuns)

# 计算某个主机上任务的平均运行时间
def getAverageRunTimeInHost(jobs: List[JobRecord], hostName: str):
    time_total = 0.0
    count = 0
    for job in jobs:
        for jobRun in job.jobRuns:
            if jobRun.host == hostName:
                time_total += jobRun.duration
                count += 1
    return time_total / count


# 计算集群的吞吐率,但是现在还是有问题
def getThroughput(jobs: List[JobRecord], cluster: ClusterRecord):
    time_total = cluster.getInUseTime()
    flops_total = 0.0
    for job in jobs:
        jobInfo = sysSim.jobs[job.jobName]
        flops_total += jobInfo.getFLOPS() * len(job.jobRuns)
    print("f:" + flops_total.__str__())
    print("t:" + time_total.__str__())
    if time_total == 0.0:
        return 0
    return  flops_total/ time_total

# 计算集群的算力利用率
def getEfficiency(jobs: List[JobRecord], cluster: ClusterRecord):
    time_total = cluster.getInUseTime()
    flops_total = 0.0
    time_total_tmp = 0.0
    for job in jobs:
        jobInfo = sysSim.jobs[job.jobName]
        flops_total += jobInfo.getFLOPS() * len(job.jobRuns)
    if time_total == 0.0:
        return 0
    return  flops_total / (time_total * sysSim.getFLOPS())