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

    def __repr__(self) -> str:
        return f"Process({self.idx}): {self.AT}, {self.BT}, {self.CT}, {self.TAT}, {self.WT}, {self.RT}"

n = int(input("Number of processes: "))
arrivalTime = list(map(int, input("Arrival Times: ").split()))
burstTime = list(map(int, input("Burst Times: ").split()))

processes = sorted([Process(x+1,arrivalTime[x],burstTime[x]) for x in range(len(arrivalTime))],key=lambda x:x.AT)
cpuTime = processes[0].AT

for p in processes:
    if(p.AT <= cpuTime):
        p.firstExecution = cpuTime
    else:
        p.firstExecution = p.AT

    p.CT = p.firstExecution + p.BT
    p.calc()
    cpuTime = p.CT

print("\nProcess, AT, BT, CT, TAT, WT, RT")
[print(x) for x in sorted(processes,key=lambda x: x.idx)]

print("\nAverage:")
print(f"CT: {sum((x.CT for x in processes))/n}")
print(f"TAT: {sum((x.TAT for x in processes))/n}")
print(f"WT: {sum((x.WT for x in processes))/n}")
print(f"RT: {sum((x.RT for x in processes))/n}\n")