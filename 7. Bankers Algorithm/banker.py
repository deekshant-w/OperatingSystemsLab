import pandas as pd
import numpy as np

cols = pd.MultiIndex.from_product(
    [
        ["Allocation", "Max", "Available", "Remaining"], 
        ["A", "B", "C"]
    ]
)

process_count = int(input("Number Of Processes: "))
index = [f"P{x+1}" for x in range(process_count)]
df = pd.DataFrame(index=index, columns=cols, dtype=np.int64)

for x in ["Allocation", "Max"]:
    for y in ["A", "B", "C"]:
        df.loc[:, (x, y)] = list(map(int, input(f"{x} {y} : ").split()))

df["Remaining"] = df["Max"] - df["Allocation"]
df["Available"] = 0

sys_resourcces = np.array(list(map(int, input("Free Resources: ").split()))).astype(np.int64)
order = []
found = 1

while len(order) < process_count:
    if not found:
        break
    found = 0
    for index, row in df.iterrows():
        if index not in order:
            if np.all(sys_resourcces >= df["Remaining"].loc[index]):
                order.append(index)
                df.loc[index, "Available"] = sys_resourcces.tolist()
                sys_resourcces += df["Allocation"].loc[index]
                found = 1

df["Available"] = df["Available"].astype(np.int64)
print(df)

if not found:
    print("System is not in safe state!")
else:
    print("System is in safe state!")
    print(*order)