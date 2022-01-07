import heapq

class Process:
    def __init__(self, idx, AT, BT,) -> None:
        self.idx = idx
        self.AT = AT
        self.BT = BT
        self.CT = None
        self.firstExecution = None

    def calc(self):
        self.TAT = self.CT - self.AT
        self.WT = self.TAT - self.BT
        self.RT = self.firstExecution - self.AT

    def __lt__(self,other):
        return self.BT<other.BT

    def __repr__(self) -> str:
        return f"Process({self.idx}): {self.AT}, {self.BT}, {self.CT}, {self.TAT}, {self.WT}, {self.RT}"

n = int(input("Number of processes: "))
arrivalTime = list(map(int, input("Arrival Times: ").split()))
burstTime = list(map(int, input("Burst Times: ").split()))

processes = sorted([Process(x+1,arrivalTime[x],burstTime[x]) for x in range(len(arrivalTime))],key=lambda x:x.AT)
heap = []
completed = []
cpuTime = processes[0].AT

for p in processes:
    while heap:
        if cpuTime>=p.AT:
            break
        
        if heap[0].AT<=cpuTime:
            heap[0].firstExecution = cpuTime
        else:
            heap[0].firstExecution = heap[0].AT

        heap[0].CT = heap[0].firstExecution + heap[0].BT
        heap[0].calc()
        cpuTime = heap[0].CT
        completed.append(heapq.heappop(heap))

    heapq.heappush(heap,p)

while heap:
    if heap[0].AT<=cpuTime:
        heap[0].firstExecution = cpuTime
    else:
        heap[0].firstExecution = heap[0].AT

    heap[0].CT = heap[0].firstExecution + heap[0].BT
    heap[0].calc()
    cpuTime = heap[0].CT
    completed.append(heapq.heappop(heap))

print("Process, AT, BT, CT, TAT, WT, RT")
[print(x) for x in sorted(completed,key=lambda x: x.idx)]

print("\nAverage:")
print(f"CT: {sum((x.CT for x in completed))/n}")
print(f"TAT: {sum((x.TAT for x in completed))/n}")
print(f"WT: {sum((x.WT for x in completed))/n}")
print(f"RT: {sum((x.RT for x in processes))/n}")