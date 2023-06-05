import os
import time

class Job:
    def __init__(self, name, burstTime, jobSize):
        self.name = name
        self.burstTime = burstTime
        self.jobSize = jobSize
        self.remainingTime = burstTime
        self.memLocation = 'Unallocated'
        self.memorysize = 0
        self.internalFrag = 0
    def __repr__(self):
        return "P" + str(self.name)
    def __str__(self):
        return "P" + str(self.name) + "(" + str(self.jobSize) + ")"
    
class MemBlock:
    def __init__(self, name, memSize):
        self.name = name
        self.memSize = memSize
        self.jobs = []
        self.queue = []
        self.status = 'Free'
        self.fragmentation = memSize
        self.totalfrag = 0
        self.waitingTime = []
        self.currentTime = []
        self.throughput = []
    def __repr__(self):
        return "M" + str(self.name)
    def __str__(self):
        return "M" + str(self.name) + "(" + str(self.memSize) + ")"

def MAT(jobList,memList):
    choice = input("\nEnter chosen Memory Allocation and Management Method: \n\n (1) First-fit \n\n (2) Best-fit \n\n (3) Worst-fit \n\n Answer: ")

    match choice:
        case "1":
            First_fit(jobList,memList)
        case "2":
            Best_fit(jobList,memList)
        case "3":
            Worst_fit(jobList,memList)

# Extract data in given files
def readJobList(filename):
    jobs = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            # Skip the header names
            if i == 0:
                continue
            # Extract values from txt file
            fields = line.strip().split()
            name = fields[0]
            burstTime = fields[1]
            jobSize = fields[2]

            job = Job(name, int(burstTime), int(jobSize))
            # print(job)
            jobs.append(job)
    return jobs

def readMemList(filename):
    blocks = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            # Skip the header names
            if i == 0:
                continue
            # Extract values from txt file
            fields = line.strip().split()
            name = fields[0]
            memSize = fields[1]

            block = MemBlock(name, int(memSize))
            # print(block)
            blocks.append(block)
    return blocks

# Display job and memory block lists
def joblist(jobs):
    print("\n\n\tProcesses: ", end="")
    count = 0
    for job in jobs:
        count += 1
        if count > 10:
            print("\n\t           ", end="")
            count = 1
        print("P" + str(job.name) + "(" + str(job.jobSize) + ")", end=" ")

def memlist(memblocks):
    print("\n\n\tMemory Partitions: ", end=" ")
    count = 0
    for block in memblocks:
        count += 1
        if count > 5:
            print("\n\t\t            ", end="")
            count = 1
        print("M" + block.name + "(" + str(block.memSize) + ")", end=" ")
    print("\n")

# Function to calculate the performance of the algorithm
def Metrics(jobs, memblocks, time, fragment, throughput):
    avg_waiting_queue = []
    avg_waiting_time_memblock = []
    never_used = []

    # Calculate performance
    completed_jobs = [job for job in jobs if job.memLocation != 'Unallocated']
    # print(throughput, sum(throughput))
    throughput_res = sum(throughput) / time
    # print(sum(throughput))
    
    totalMem = sum(block.memSize for block in memblocks)
    usedMem = sum(job.jobSize for job in jobs)
    fragMem = sum(block.totalfrag for block in memblocks)
    remMem = usedMem - fragMem
    # print(totalMem, usedMem, fragMem, remMem)
    storage_utilization = remMem / usedMem * 100
    # storage_utilization = remMem / totalMem * 100
 
    # Print Allocation Technique Performance
    print("\n\n")
    print("=============== Metrics ===============".center(135))
    print(f"\n\tThroughput: {throughput_res:.2f} jobs per time unit")
    print(f"\n\tWaiting Queue Length Total: ")
    print(f"\tThe number of jobs that were assigned to each partition are the following..")
    for block in memblocks:
        if len(block.jobs) > 0:
            waitingQ_len = len(block.jobs)
            avg_waiting_queue.append(waitingQ_len)
            waiting_time = sum(block.waitingTime)
            avgwaiting_time = waiting_time / waitingQ_len
            avg_waiting_time_memblock.append(avgwaiting_time)
            print(f"\t=---= M{block.name} : {waitingQ_len} job\s\t | Average Waiting Time in Queue: {avgwaiting_time:.2f} ms")
        else:
            print(f"\t=---= M{block.name} : No jobs allocated")
            never_used.append(block)

    used_partitions = [block for block in memblocks if len(block.jobs) > 1]
    st_util1 = (len(never_used) / len(memblocks)) * 100
    st_util2 = 100 - st_util1
    st_util3 = (len(used_partitions) / (len(memblocks) - len(never_used))) * 100
    print(f"\n\tStorage Utilization: {storage_utilization:.2f}%")
    print(f"\tPercentage of partitions used: {st_util2}%")
    print(f"\tPercentage of partitions heavily used: {st_util3:.2f}% of partitions used")
    print(f"\tPercentage of partitions never used: {st_util1}%")

    avg_waiting_queue = sum(avg_waiting_queue) / len(avg_waiting_queue)
    avg_waiting_time_memblock = sum(avg_waiting_time_memblock) / len(avg_waiting_time_memblock)
    print(f"\n\tAverage Waiting Queue Length: {avg_waiting_queue:.2f} jobs")

    print(f"\n\tAverage Waiting Time for all Partitions: {avg_waiting_time_memblock:.2f} ms")
    print(f"\n\tInternal Fragmentation: ")
    for block in memblocks:
        if len(block.jobs) > 0:
            print(f"\t=---= M{block.name} : {block.totalfrag} k")
    print(f"\tTotal Internal Fragmentation: {fragment} k")

# Function to display the status of each process
def display_blocks(memblocks):
    print("\n\n\t\t| Memory Block | Memory Size | Status | ")

    for block in memblocks:
        print(f"\t\t       M{block.name}\t     {str(block.fragmentation)}\t{str(block.status)}")

def display(jobs, memblocks, completedJobs, unallocatable, algo, time_unit, allocated):
    # time.sleep(0.1) 
    os.system("cls")
    print("\n")
    if algo == 'First-fit':
        print("========== First-fit ==========".center(135))
    elif algo == 'Best-fit':
        print("========== Best-fit ==========".center(135))
    elif algo == 'Worst-fit':
        print("========== Worst-fit ==========".center(135))
    # joblist(jobs)
    # memlist(memblocks)
    print(f"\n\t\tTime Elapsed: {time_unit} s\n")
    display_blocks(memblocks)

    print("\n\n\t\t| Process | Job Size | Memory Partition | Memory Size | Internal Fragmentation | Duration | ")
    for job in jobs:
        if job.remainingTime == 0:
            print(f"\t\t    P{job.name}\t      {str(job.jobSize)}\t  {str(job.memLocation).center(10)}\t{str(job.memorysize).center(15)}\t      {str(job.internalFrag).center(10)}\t{str('-').center(10)}")
        else:
            print(f"\t\t    P{job.name}\t      {str(job.jobSize)}\t  {str(job.memLocation).center(10)}\t{str(job.memorysize).center(15)}\t      {str(job.internalFrag).center(10)}\t{str(job.remainingTime).center(10)}")
    print("\n\t\tCompleted Jobs: " + str(completedJobs))
    print("\t\tUnallocatable Jobs: " + str(unallocatable))

    # for block in memblocks:
    #     print(f"\nM{block.name} : {block.queue}")
    throughput = len(completedJobs)
    print(f"\n\t\t==Throughput==")
    print(f"\t\tJobs Completed: {throughput}")
    print(f"\t\tJobs allocated: {allocated} job\s")
    used_partitions = [block for block in memblocks if len(block.queue) >= 1]
    unused_partitions = [block for block in memblocks if len(block.queue) == 0]
    st_util1 = (len(unused_partitions) / len(memblocks)) * 100
    st_util2 = (len(used_partitions) / len(memblocks)) * 100
    # print(f"\n\tStorage Utilization: {storage_utilization:.2f}%")
    print(f"\n\t\t==Storage Utilization==")
    print(f"\t\tPercentage of partitions used: {st_util2}%")
    print(f"\t\tPercentage of partitions not used: {st_util1}%")

def simulate(jobs, memblocks, algo):

    completedJobs = []
    unallocatable = []
    executing = []
    throughput = []
    allocatedBlocks = {block.name: None for block in memblocks}
    maxMemory = max(block.memSize for block in memblocks)
    time_unit = -1
    total_Intfragment = 0
    allocated = 0
    processing = 0

    # Apply First-fit memory allocation technique and Print Output
    while len(completedJobs) + len(unallocatable) < len(jobs):
        # For time-unit by time-unit checking, uncomment input()
        input()
        time_unit += 1
        throughput.append(processing)
        # print(throughput)
        allocated = 0
        if algo == 'Best-fit':
            processing = 0.5
        else:
            processing = 0

        for job in jobs:
            if algo == 'First-fit':
                sorted_mblocks = memblocks
            elif algo == 'Best-fit':
                sorted_mblocks = sorted(memblocks, key=lambda x: x.memSize)
            elif algo == 'Worst-fit':
                sorted_mblocks = sorted(memblocks, key=lambda x: x.memSize, reverse=True)

            if job not in completedJobs:
                # Handle jobs that are larger than all available memory partitions
                if job.jobSize > maxMemory:
                    job.memorysize = '-'
                    job.internalFrag = '-'
                    if job not in unallocatable:
                        unallocatable.append(job)
                
                if job.memLocation != 'Unallocated':
                    processing += 1
                    
                for block in sorted_mblocks:
                    # Allocate Processes to free memory blocks 
                    if allocatedBlocks[block.name] is None and block.memSize >= job.jobSize and job.memLocation == 'Unallocated':
                        
                        # Initializations
                        allocatedBlocks[block.name] = job
                        job.memLocation = block.name
                        job.memorysize = block.memSize
                        block.memSize -= job.jobSize
                        job.internalFrag = block.memSize
                        block.status = "P"+str(job.name)
                        block.fragmentation = block.memSize
                        total_Intfragment += block.fragmentation
                        block.totalfrag += block.fragmentation
                        
                        # Appends
                        executing.append(job)
                        block.jobs.append(job)
                        block.queue.append(job)
                        block.waitingTime.append(job.burstTime)

                        allocated += 1
                        display(jobs, memblocks, completedJobs, unallocatable, algo, time_unit, allocated)
                        break
                    
                    elif allocatedBlocks[block.name] == job:
                        if job in executing:
                            if job.remainingTime > 0:
                                job.remainingTime -= 1
                        # Check whether job has expired
                        if job.remainingTime == 0:
                            completedJobs.append(job)
                            allocatedBlocks[block.name] = None # Indicate that the memory block is free
                            job.memLocation = "Completed"
                            job.memorysize = "-"
                            job.internalFrag = "-"
                            block.status = 'Free'
                            block.memSize += job.jobSize # Return the memory back to its original size
                            block.fragmentation = block.memSize
                            executing.remove(job)
                            block.queue.remove(job)
                        display(jobs, memblocks, completedJobs, unallocatable, algo, time_unit, allocated)
                        break
    Metrics(jobs, memblocks, time_unit, total_Intfragment, throughput)
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Memory Allocation Techniques

def First_fit(jobList,memList):
    os.system("cls")
    jobs = readJobList(jobList)
    memblocks = readMemList(memList)
    algo = 'First-fit'
    simulate(jobs, memblocks, algo)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def Best_fit(jobList,memList):
    os.system("cls")
    jobs = readJobList(jobList)
    memblocks = readMemList(memList)
    algo = 'Best-fit'
    simulate(jobs, memblocks, algo)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def Worst_fit(jobList,memList):
    os.system("cls")
    jobs = readJobList(jobList)
    memblocks = readMemList(memList)
    algo = 'Worst-fit'
    simulate(jobs, memblocks, algo)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
jobs = 'job_list.txt'
MemBlocks = 'mem_list.txt'
MAT(jobs, MemBlocks)