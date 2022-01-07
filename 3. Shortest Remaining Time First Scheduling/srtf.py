import heapq

class Process:
    def __init__(self, idx, AT, BT,) -> None:
        self.idx = idx
        self.AT = AT
        self.BT = BT
        self.remaining = BT
        self.CT = None
        self.firstExecution = None

    def calc(self):
        self.TAT = self.CT - self.AT
        self.WT = self.TAT - self.BT
        self.RT = self.firstExecution - self.AT

    def __lt__(self,other):
        if self.remaining==other.remaining:
            return self.AT<other.AT
        return self.remaining<other.remaining

    def __repr__(self) -> str:
        return f"Process({self.idx}): {self.AT}, {self.BT}, {self.CT}, {self.TAT}, {self.WT}, {self.RT}"

n = int(input("Number of processes: "))
arrivalTime = list(map(int, input("Arrival Times: ").split()))
burstTime = list(map(int, input("Burst Times: ").split()))

processes = sorted([Process(x+1,arrivalTime[x],burstTime[x]) for x in range(len(arrivalTime))],key=lambda x:x.AT)
processID = 0
heap = []
completed = []
cpuTime = processes[0].AT

while len(completed)<n:
    for p in range(processID,n):
        p = processes[p]
        if(p.AT<=cpuTime):
            heapq.heappush(heap,p)
            processID+=1
        else:
            break

    cpuTime+=1

    if heap:
        heap[0].remaining-=1
        if heap[0].firstExecution == None:
            heap[0].firstExecution = cpuTime-1
        if heap[0].remaining==0:
            heap[0].CT = cpuTime
            heap[0].calc()
            completed.append(heapq.heappop(heap))


print("Process, AT, BT, CT, TAT, WT, RT")
[print(x) for x in sorted(completed,key=lambda x: x.idx)]

print("\nAverage:")
print(f"CT: {sum((x.CT for x in completed))/n}")
print(f"TAT: {sum((x.TAT for x in completed))/n}")
print(f"WT: {sum((x.WT for x in completed))/n}")
print(f"RT: {sum((x.RT for x in processes))/n}")