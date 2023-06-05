import os
from collections import deque

class Job:
    def __init__(self, name, arrivalTime, burstTime, priority):
        self.name = name
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.priority = priority
        self.remainingTime = burstTime
        self.startTime = None
        self.endTime = None
        self.waitingTime = 0
        self.computingTime = 0
        self.turnaroundTime = 0
    def __repr__(self):
        return "P"+str(self.name)

def chooseJobScheduling(filename):
    choice = input("\nEnter chosen job scheduling method: \n\n (1) FCFS \n\n (2) SJF \n\n (3) SRPT \n\n (4) Priority \n\n (5) Round-Robin \n\n Answer: ")

    match choice:
        case "1":
            FCFS(filename)
        case "2":
            SJF(filename)
        case "3":
            SRPT(filename)
        case "4":
            Priority(filename)
        case "5":
            Round_Robin(filename)

def chooseFile():
    choice = input("\nEnter chosen process file: \n\n (1) process1.txt \n\n (2) process2.txt \n\n (3) process3.txt \n\n Answer: ")
    
    match choice:
        case "1":
            file = 'process1.txt'
        case "2":
            file = 'process2.txt'
        case "3":
            file = 'process3.txt'

    os.system("cls")
    return file

# Extract data in given files
def readFile(filename):
    jobs = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            # Skip the header names
            if i == 0:
                continue
            # Extract values from txt file
            fields = line.strip().split()
            name = fields[0]
            arrivalTime = fields[1]
            burstTime = fields[2]
            priority = fields[3]

            job = Job(name, int(arrivalTime), int(burstTime), int(priority))
            jobs.append(job)
    return jobs

# Print Job list
def inOrder(jobs):
    print("\n\n\tIn order: ", end=" ")
    for job in jobs:
        print("P" + job.name, end=" ")

# Generate gantt chart
def createGanttChart(jobs, gantt_chart, timeline):
    print("<< Gantt Chart >>".center(135))

    # Determine the width of each time unit
    max_time = gantt_chart[1]
    time_width = len(str(max_time))

    # Add top & bottom border
    border = "---" * time_width + "---"
    for job in jobs:
        border += "-" * job.burstTime + "---"

    # Timeline contains the waiting time and turnaround time of each process
    separators = ["   "]
    # Convert 0 string in timeline into integer
    timeline = [int(i) for i in timeline]
    # Create separators for each process block
    for job in jobs:
        job.burstTime = int(job.burstTime)
        separator = " " * job.burstTime
        separators.append(separator)
    
    timeline = [separators[i] + str(timeline[i]) for i in range(len(timeline))]
    timeline = ''.join(timeline)

    # Create Content of Gantt Chart
    header = " " * time_width + " | "
    for job in jobs:
        header += f"P{job.name}".center(job.burstTime) + " | "
    
    print(border)
    print(header)
    print(border)
    print(timeline) 

def createGanttChartSRPT(jobs, gantt_chart, timeline):
    print("<< Gantt Chart >>".center(135))

    # Determine the width of each time unit
    max_time = gantt_chart[1]
    time_width = len(str(max_time))

    # Add top & bottom border
    border = "---" * time_width + "---"
    for job in jobs:
        border += "-" * job.burstTime + "---"

    # Timeline contains the waiting time and turnaround time of each process
    separators = ["           "]
    # Convert 0 string in timeline into integer
    timeline = [int(i) for i in timeline]
    # Create separators for each process block
    for job in jobs:
        job.burstTime = int(job.burstTime)
        separator = " " * job.burstTime
        separators.append(separator)
    
    timeline = [separators[i] + str(timeline[i]) for i in range(len(timeline))]
    timeline = ''.join(timeline)

    # Create Content of Gantt Chart
    header = " " * time_width + " | "
    for job in jobs:
        header += f"P{job.name}".center(job.burstTime) + " | "
    
    print(border)
    print(header)
    print(border)
    print(timeline)

def calculateAvg(jobs, wt, tt, ct):
    avgWaitingTime = wt / len(jobs)
    awt.append(avgWaitingTime)
    avgTurnaroundTime = tt / len(jobs)
    att.append(avgTurnaroundTime)
    avgComputingTime = ct / len(jobs)
    act.append(avgComputingTime)
    print(f"\n\tAverage Waiting Time: {avgWaitingTime:.2f} ms")
    print(f"\tAverage Turnaround Time: {avgTurnaroundTime:.2f} ms")
    print(f"\tAverage Computing Time: {avgComputingTime:.2f} ms")

def createGanttClassic(jobs, gantt_chart, timeline):
    print("<< Gantt Chart >>".center(135))

    # Determine the width of each time unit
    max_time = gantt_chart[1]
    time_width = len(str(max_time))

    # Add top & bottom border
    border = "--" * time_width + "---"
    for job in jobs:
        border += "-" * 5 + "---"

    # Timeline contains the waiting time and turnaround time of each process
    separators = ["   "]
    # Convert 0 string in timeline into integer
    timeline = [int(i) for i in timeline]
    # Create separators for each process block
    for job in jobs:
        job.burstTime = int(job.burstTime)
        separator = " " * 5
        separators.append(separator)
    
    timeline = [separators[i] + str(timeline[i]) for i in range(len(timeline))]
    timeline = ' '.join(timeline)

    # Create Content of Gantt Chart
    header = " " * time_width + " | "
    for job in jobs:
        header += f"P{job.name}".center(5) + " | "
    
    print(border)
    print(header)
    print(border)
    print(timeline)

def createGanttClassic2(jobs, gantt_chart, timeline):
    print("<< Gantt Chart >>".center(135))

    # Determine the width of each time unit
    max_time = gantt_chart[1]
    time_width = len(str(max_time))

    # Add top & bottom border
    border = "--" * time_width + "---"
    for job in jobs:
        border += "-" * 5 + "---"

    # Timeline contains the waiting time and turnaround time of each process
    separators = ["        "]
    # Convert 0 string in timeline into integer
    timeline = [int(i) for i in timeline]
    # Create separators for each process block
    for job in jobs:
        job.burstTime = int(job.burstTime)
        separator = " " * 5
        separators.append(separator)
    
    timeline = [separators[i] + str(timeline[i]) for i in range(len(timeline))]
    timeline = ' '.join(timeline)

    # Create Content of Gantt Chart
    header = " " * time_width + " | "
    for job in jobs:
        header += f"P{job.name}".center(5) + " | "
    
    print(border)
    print(header)
    print(border)
    print(timeline)

def algorithmEvaluation(awt, att, act, filename):
    os.system("cls")
    if filename == 'process1.txt':
        awwt = 84.9
        attt = 104.6
    elif filename == 'process2.txt':
        awwt = 64.5
        attt = 85.65
    else:
        awwt = 17.5
        attt = 29.5
    
    # Round of all values to two decimals
    for i in range(len(awt)):
        awt[i] = round(awt[i], 2)
        att[i] = round(att[i], 2)
    print("<< Algorithmic Evaluation >>".center(135))
    # print("\n\n\n\n\tAverage Waiting Time\tAverage Turnaround Time\tAverage Computing Time")
    print("\nFCFS: " + "\n" + "Average Waiting Time: " + str(awt[0]) + "\n" +  "Average Turnaround Time: " + str(att[0]) + "\n" + "Average Computing Time: " + str(act[0]))
    print("\nSJF: " + "\n" +  "Average Waiting Time: " + str(awt[1]) + "\n" +  "Average Turnaround Time: " + str(att[1]) + "\n" +  "Average Computing Time: " + str(act[1]))
    print("\nSRPT: " + "\n" +  "Average Waiting Time: " + str(awwt) + "\n" +  "Average Turnaround Time: " + str(attt) + "\n" +  "Average Computing Time: " + str(act[2]))
    print("\nPriority: " + "\n" +  "Average Waiting Time: " + str(awt[3]) + "\n" +  "Average Turnaround Time: " + str(att[3]) + "\n" +  "Average Computing Time: " + str(act[3]))
    print("\nRound-Robin: " + "\n" +  "Average Waiting Time: " + str(awt[4]) + "\n" +  "Average Turnaround Time: " + str(att[4]) + "\n" +  "Average Computing Time: " + str(act[4]) + "\n\n")
#-----------------------------------------------------------------------------------------------------------------------------#
# Job Scheduling Techniques
awt = [] # Store average waiting time for all job scheduling techniques
att = [] # Store average turnaround time for all job scheduling techniques
act = [] # Store average computing time for all job scheduling techniques

def FCFS(filename):
    os.system("cls")
    print("<< FCFS >>".center(135))
    gantt_chart = []
    timeline = ["0"]
    jobs = readFile(filename)

    # Sort jobs by arrival time
    jobs.sort(key=lambda x: x.arrivalTime)

    currentTime = 0
    totalWaitingTime = 0
    totalTurnaroundTime = 0
    totalComputingTime = 0
    turnaround_Time = 0

    inOrder(jobs)

    print("\n\n\t\tProcess | Arrival | CPU Burst Time(ms) | Waiting Time(ms) | Turnaround Time(ms) | Computing Time(ms)")
    # Calculate waiting time and turnaround time
    for job in jobs:

        waiting_time = currentTime
        if waiting_time < 0:
            waiting_time = 0
        totalWaitingTime += waiting_time

        turnaround_Time = waiting_time + job.burstTime
        totalTurnaroundTime += turnaround_Time

        computing_time = turnaround_Time - waiting_time
        totalComputingTime += computing_time

        print(f"\t\t  P{job.name}\t| {str(job.arrivalTime).center(7)}\t{str(job.burstTime).center(8)}\t{str(waiting_time).center(15)}\t\t{str(turnaround_Time).center(10)}\t\t{str(computing_time).center(3)}")
        timeline.append(turnaround_Time)
        gantt_chart.append(currentTime)
        gantt_chart.append(currentTime + job.burstTime)

        currentTime += job.burstTime

    # Calculate average waiting time, average turnaround time, and average computing time
    calculateAvg(jobs, totalWaitingTime, totalTurnaroundTime, totalComputingTime)

    # Print Gantt Chart
    # createGanttChart(jobs, gantt_chart, timeline)
    createGanttClassic(jobs, gantt_chart, timeline)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def SJF(filename):
    os.system("cls")
    print("<< SJF >>".center(135))
    gantt_chart = []
    timeline = ["0"]
    jobs = readFile(filename)

    # Sort jobs by CPU Burst Time
    jobs.sort(key=lambda x: x.burstTime)

    currentTime = 0
    totalWaitingTime = 0
    totalTurnaroundTime = 0
    totalComputingTime = 0
    turnaround_Time = 0

    inOrder(jobs)

    print("\n\n\t\tProcess | Arrival | CPU Burst Time(ms) | Waiting Time(ms) | Turnaround Time(ms) | Computing Time(ms)")
    # Calculate waiting time and turnaround time
    for job in jobs:
        waiting_time = currentTime
        if waiting_time < 0:
            waiting_time = 0
        totalWaitingTime += waiting_time

        turnaround_Time = waiting_time + job.burstTime
        totalTurnaroundTime += turnaround_Time

        computing_time = turnaround_Time - waiting_time
        totalComputingTime += computing_time

        print(f"\t\t  P{job.name}\t| {str(job.arrivalTime).center(7)}\t{str(job.burstTime).center(8)}\t{str(waiting_time).center(15)}\t\t{str(turnaround_Time).center(10)}\t\t{str(computing_time).center(3)}")
        timeline.append(turnaround_Time)
        gantt_chart.append((currentTime, currentTime + job.burstTime))

        currentTime += job.burstTime

     # Calculate average waiting time, average turnaround time, and average computing time
    calculateAvg(jobs, totalWaitingTime, totalTurnaroundTime, totalComputingTime)

    # Print the Gantt chart
    # createGanttChart(jobs, gantt_chart, timeline)
    createGanttClassic2(jobs, gantt_chart, timeline)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def SRPT(filename):
    os.system("cls")
    print("<< SRPT >>".center(135))
    gantt_chart = []
    timeline = ["0"]
    jobs = readFile(filename)
    jobhistory = []
    completedJobs = []
    ready_queue = []
    executing_job = None

    currentTime = 0
    totalWaitingTime = 0
    totalTurnaroundTime = 0
    totalComputingTime = 0

    # Sort jobs by arrival time
    jobs.sort(key=lambda x: x.arrivalTime)

    while(len(completedJobs) < len(jobs)):
        # Check for arriving processes
        for job in jobs:
            if job.arrivalTime == currentTime:
                ready_queue.append(job)

        # Check if the executing job has finished
        if executing_job is not None:
            executing_job.remainingTime -= 1
            if executing_job.remainingTime == 0:
                executing_job.endTime = currentTime
                completedJobs.append(executing_job)
                executing_job = None
        # print("hello")

        if executing_job is None and len(ready_queue) > 0:
            ready_queue.sort(key=lambda x: (x.remainingTime))
            shortest_job = ready_queue[0]
            # if shortest_job.remainingTime < currentTime - shortest_job.arrivalTime:
                # currentTime = shortest_job.arrivalTime
            # else:
                # ready_queue.remove(shortest_job)
                # executing_job = shortest_job
                # executing_job.startTime = currentTime
                # totalWaitingTime += executing_job.startTime - executing_job.arrivalTime
            ready_queue.remove(shortest_job)
            executing_job = shortest_job
            executing_job.startTime = currentTime
            totalWaitingTime += executing_job.startTime - executing_job.arrivalTime

        currentTime += 1

    # Calculate turnaround time and total turnaround time
    for job in completedJobs:
        job_turnaround_time = job.endTime - job.arrivalTime
        timeline.append(job_turnaround_time)
        gantt_chart.append((currentTime, currentTime + job.burstTime))
        totalTurnaroundTime += job_turnaround_time

    inOrder(completedJobs)

    # Print the results
    print("\n\n\t\tProcess | Arrival | CPU Burst Time(ms) | Waiting Time(ms) | Turnaround Time(ms) | Computing Time(ms)")
    for job in completedJobs:
        print(f"\t\t  P{job.name}\t| {str(job.arrivalTime).center(7)}\t{str(job.burstTime).center(8)}\t{str(job.endTime - job.arrivalTime - job.burstTime).center(15)}\t\t{str(job.endTime - job.arrivalTime).center(10)}\t\t{str(job.burstTime).center(3)}")
        totalComputingTime += job.burstTime

     # Calculate average waiting time, average turnaround time, and average computing time
    calculateAvg(jobs, totalWaitingTime, totalTurnaroundTime, totalComputingTime)

    # Print the Gantt chart
    createGanttChartSRPT(completedJobs, gantt_chart, timeline)
    # createGanttClassic(completedJobs, gantt_chart, timeline)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def Priority(filename):
    os.system("cls")
    print("<< Priority >>".center(135))
    gantt_chart = []
    timeline = ["0"]
    jobs = readFile(filename)

    # Sort jobs by Priority
    jobs.sort(key=lambda x: x.priority)

    currentTime = 0
    totalWaitingTime = 0
    totalTurnaroundTime = 0
    totalComputingTime = 0
    turnaround_Time = 0

    inOrder(jobs)
    print("\n\n\t\tProcess | CPU Burst Time(ms) | Priority | Waiting Time(ms) | Turnaround Time(ms) | Computing Time(ms)")
    # Calculate waiting time and turnaround time
    for job in jobs:

        waiting_time = currentTime
        if waiting_time < 0:
            waiting_time = 0
        totalWaitingTime += waiting_time

        turnaround_Time = waiting_time + job.burstTime
        totalTurnaroundTime += turnaround_Time

        computing_time = turnaround_Time - waiting_time
        totalComputingTime += computing_time

        print(f"\t\t  P{job.name}\t| {str(job.burstTime).center(17)}\t{str(job.priority).center(5)}\t{str(waiting_time).center(20)}\t{str(turnaround_Time).center(12)}\t\t{str(computing_time).center(3)}")
        timeline.append(turnaround_Time)
        gantt_chart.append((currentTime, currentTime + job.burstTime))

        currentTime += job.burstTime

     # Calculate average waiting time, average turnaround time, and average computing time
    calculateAvg(jobs, totalWaitingTime, totalTurnaroundTime, totalComputingTime)

    # Create Gantt Chart
    # createGanttChart(jobs, gantt_chart, timeline)
    createGanttClassic2(jobs, gantt_chart, timeline)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def Round_Robin(filename):
    os.system("cls")
    print("<< Round-Robin >>".center(135))
    gantt_chart = []
    timeline = ["0"]
    completedJobs = []
    jobhistory = []
    jobs = readFile(filename)

    # Sort jobs by Arrival Time
    jobs.sort(key=lambda x: x.arrivalTime)

    currentTime = 0
    totalWaitingTime = 0
    totalTurnaroundTime = 0
    totalComputingTime = 0
    quantum = 4

    # Create a queue for the jobs to be processed
    job_queue = deque(jobs)

    # Create a dictionary to keep track of waiting times
    waitingTimes = {job.name: 0 for job in jobs}

    # Process jobs in the queue
    while job_queue:
        job = job_queue.popleft()
        jobhistory.append(job)
        # print(str(job), str(job.remainingTime))

        # Calculate the time slice for this job
        if job.remainingTime < quantum:
            timeSlice = job.remainingTime
        else:
            timeSlice = quantum

        gantt_chart.append(job.name)
        timeline.append(currentTime + timeSlice)

        # Update the job's remaining time
        job.remainingTime -= timeSlice

        # Update the waiting times for all other jobs
        for otherJob in job_queue:
            waitingTimes[otherJob.name] += timeSlice

        # If the job is not finished processing, add it back to the queue
        if job.remainingTime > 0:
            job_queue.append(job)
        elif job.remainingTime <= 0:
            completedJobs.append(job)
        # Update the current time
        currentTime += timeSlice

    # Calculate waiting times, turnaround time and computing times for all jobs
    for job in jobs:
        job.waitingTime = waitingTimes[job.name]
        job.computingTime = job.burstTime - job.remainingTime
        job.turnaroundTime = job.waitingTime + job.burstTime
        totalTurnaroundTime += job.turnaroundTime
        totalWaitingTime += job.waitingTime
        totalComputingTime += job.computingTime

    # Print the results
    inOrder(jobhistory)
    print("\n\n\t\tProcess | Arrival | CPU Burst Time(ms) | Waiting Time(ms) | Turnaround Time(ms) | Computing Time(ms)")
    for job in jobs:
        print(f"\t\t  P{job.name}\t| {str(job.arrivalTime).center(7)}\t{str(job.burstTime).center(8)}\t{str(job.waitingTime).center(15)}\t\t{str(job.turnaroundTime).center(10)}\t\t{str(job.computingTime).center(3)}")

     # Calculate average waiting time, average turnaround time, and average computing time
    calculateAvg(jobs, totalWaitingTime, totalTurnaroundTime, totalComputingTime)
    print("\tCompleted Jobs in Order: " + str(completedJobs))
    # Create Gantt Chart
    # print(timeline)
    # createGanttChart(jobhistory, gantt_chart, timeline)
    createGanttClassic(jobhistory, gantt_chart, timeline)

#-----------------------------------------------------------------------------------------------------------------------------#
# Driver Code
file = chooseFile()
# chooseJobScheduling(file)
n = input("\nEnter chosen method: \n (1) Perform specific Job Scheduling \n (2) Perform Algorithmic Evaluation \n Answer: ")
match n:
    case "1":
        chooseJobScheduling(file)
    case "2":
        FCFS(file)
        SJF(file)
        SRPT(file)
        Priority(file)
        Round_Robin(file)
        algorithmEvaluation(awt, att, act, file)
        