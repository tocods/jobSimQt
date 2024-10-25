from jobSimPainter import HostRecord, HostUtilization, JobRecord, JobRun, FaultRecord
from jobSim import 
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


# 计算集群的吞吐率
def getThroughput(jobs: List[JobRecord]):
    time_total = 0.0

    for job in jobs:
        for jobRun in job.jobRuns:
            time_total += jobRun.duration
    return len(jobs) / time_total
    



