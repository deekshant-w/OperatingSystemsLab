import heapq

class Process:
    def __init__(self, idx, AT, BT, priority) -> None:
        self.idx = idx
        self.AT = AT
        self.BT = BT
        self.CT = None
        self.priority = priority
        self.firstExecution = None

        # record remaining time as algorithm is premptive,
        # hence any process can be stopped in between
        self.remaining = BT

    def calc(self) -> None:
        self.TAT = self.CT - self.AT
        self.WT = self.TAT - self.BT
        self.RT = self.firstExecution - self.AT

    def __lt__(self,other) -> bool:
        if self.priority==other.priority:
            return self.AT<other.AT
        return self.priority<other.priority

    def __repr__(self) -> str:
        return f"Process({self.idx}): {self.AT}, {self.BT}, {self.priority}, {self.CT}, {self.TAT}, {self.WT}, {self.RT}"

n = int(input("Number of processes: "))
arrivalTime = list(map(int, input("Arrival Times: ").split()))
burstTime = list(map(int, input("Burst Times: ").split()))
priority = list(map(int, input("Priorities: ").split()))

processes = sorted([Process(x+1,arrivalTime[x],burstTime[x],priority[x]) for x in range(len(arrivalTime))],key=lambda x:x.AT)

# as deletion in list is not allowed 
# while iterating using for loop, hence 
# keep a pointer to rember till which idx process are arrived
# pointer would be linear as process are already sorted using AT
processID = 0

heap = []
completed = []
cpuTime = processes[0].AT

while len(completed)<n:
    # Processes arriving
    for p in range(processID,n):
        p = processes[p]
        if(p.AT<=cpuTime):
            heapq.heappush(heap,p)
            processID+=1
        else:
            break

    cpuTime+=1

    # Arrival done for that second
    # solving cpu processing for past second
    if heap:
        # topmost process gets processed for 1 sec,
        # based on old and new process that arrived in the 
        # past second
        heap[0].remaining-=1

        # if the process is encountered first time
        if heap[0].firstExecution == None:
            # -1 as it was processded in the previous second of cpuTime
            heap[0].firstExecution = cpuTime-1
        
        # process complete
        if heap[0].remaining==0:
            # no -1 as the process was completed after
            #  the previous cpuTime second hence -> now
            heap[0].CT = cpuTime
            heap[0].calc()
            completed.append(heapq.heappop(heap))

# outputs
print("Process, AT, BT, Priority, CT, TAT, WT, RT")
[print(x) for x in sorted(completed,key=lambda x: x.idx)]

print("\nDeekshant Wadhwa- 01296303118")
print("\nAverage:")
print(f"CT: {sum((x.CT for x in completed))/n}")
print(f"TAT: {sum((x.TAT for x in completed))/n}")
print(f"WT: {sum((x.WT for x in completed))/n}")
print(f"RT: {sum((x.RT for x in processes))/n}")