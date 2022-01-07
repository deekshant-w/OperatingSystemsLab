from collections import deque

class Process:
    def __init__(self, idx, AT, BT):
        self.idx = idx
        self.AT = AT
        self.BT = BT
        self.CT = None
        self.firstExecution = None
        self.remaining = BT

    def calc(self):
        self.TAT = self.CT - self.AT
        self.WT = self.TAT - self.BT
        self.RT = self.firstExecution - self.AT

    def __repr__(self) -> str:
        return f"Process({self.idx}): {self.AT}, {self.BT}, {self.CT}, {self.TAT}, {self.WT}, {self.RT}"
        # return f"Process({self.idx}): {self.AT}, {self.BT}, {self.firstExecution}, {self.remaining}"
        

n = int(input("Number of processes: "))
r = int(input("Round Robin: "))
arrivalTime = list(map(int, input("Arrival Times: ").split()))
burstTime = list(map(int, input("Burst Times: ").split()))

processes = sorted([Process(x+1,arrivalTime[x],burstTime[x]) for x in range(len(arrivalTime))],key=lambda x:x.AT)
waitQueue = deque()
completed = []
arrivalIndex = 0
rotate = 0
cpuTime = processes[0].AT

while arrivalIndex<n or waitQueue:
    # CPU processing
    if waitQueue:
        # print(waitQueue[0])
        # First Execution
        if waitQueue[0].firstExecution is None:
            waitQueue[0].firstExecution = cpuTime

        # preemption
        if waitQueue[0].remaining > r:
            waitQueue[0].remaining -= r
            cpuTime+=r
            rotate=1

        # processing complete
        else:
            cpuTime+=waitQueue[0].remaining
            waitQueue[0].CT = cpuTime
            waitQueue[0].calc()
            completed.append(waitQueue.popleft())

    # new arrivals
    for i in range(arrivalIndex,n):
        process = processes[i]
        if process.AT <= cpuTime:
            waitQueue.append(process)
            arrivalIndex+=1
        else:
            break

    # if processess preempted
    if rotate:
        waitQueue.rotate(-1)
        rotate = 0


print("Process, AT, BT, CT, TAT, WT, RT")
[print(x) for x in sorted(completed,key=lambda x: x.idx)]

print("\nDeekshant Wadhwa- 0129633118")
print("\nAverage:")
print(f"CT: {sum((x.CT for x in completed))/n}")
print(f"TAT: {sum((x.TAT for x in completed))/n}")
print(f"WT: {sum((x.WT for x in completed))/n}")
print(f"RT: {sum((x.RT for x in processes))/n}")


