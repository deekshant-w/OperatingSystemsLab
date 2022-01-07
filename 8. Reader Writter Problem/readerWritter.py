import time
import threading
from datetime import datetime
import atexit


def timestamp(data, typ, process, i="/"):
    typ = "Reader " if typ == "r" else "Writter"
    print(f'{datetime.now().strftime("%X")} : {typ} {process} : Iteration {i} : {data}')

def exit_handler(start):
    t = round((time.perf_counter_ns() - start)/(10**9), 2)
    print(f"\nFinished... in {t}s\n")

class Problem:
    def __init__(
        self,
        readers,
        readerStart,
        readerWait,
        readerEnd,
        readerRepeat,
        writters,
        writerData,
        writterStart,
        writterWait,
        wriiterEnd,
        writterRepeat,
    ):
        """
        Reader Writter Problem
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
        readers         - int   - number of readers 
        readerStart     - list  - waiting time before reader starts 
        readerWait      - list  - waiting time before reading data 
        readerEnd       - list  - waiting time after reading data
        readerRepeat    - list  - number of time reader reades data

        writters        - int   - number of writters
        writerData      - list  - data to be written by writter
        writterStart    - list  - waiting time before writter starts writting
        writterWait     - list  - waiting time before writting
        wriiterEnd      - list  - waiting time after writting
        writterRepeat   - list  - number of times writter writes

        val             - list  - value to be written/read
        rdCount         - list  - number of writters currently in critical section
        """

        self.readers = readers
        self.readerStart = readerStart
        self.readerWait = readerWait
        self.readerEnd = readerEnd
        self.readerRepeat = readerRepeat

        self.writters = writters
        self.writerData = writerData
        self.writterStart = writterStart
        self.writterWait = writterWait
        self.wriiterEnd = wriiterEnd
        self.writterRepeat = writterRepeat

        self.val = -1
        self.rdCount = 0

        self.start()

    def start(self):
        # Writters
        for i in range(self.writters):
            threading.Thread(
                target=self.writter,
                args=(
                    i + 1,
                    self.writterStart[i],
                    self.writterWait[i],
                    self.wriiterEnd[i],
                    self.writterRepeat[i],
                    self.writerData[i],
                ),
            ).start()

        # Readers
        for i in range(self.readers):
            threading.Thread(
                target=self.reader,
                args=(
                    i + 1,
                    self.readerStart[i],
                    self.readerStart[i],
                    self.readerEnd[i],
                    self.readerRepeat[i],
                ),
            ).start()

    def wait(self):
        time.sleep(0.001)

    def reader(self, idx, start, wait, end, repeat):
        time.sleep(start)
        timestamp("started", "r", idx)
        for i in range(repeat):
            waitOne = 0
            while self.rdCount < 0:
                if waitOne:
                    waitOne = 1
                    timestamp(f"waiting", "r", idx, i)
                self.wait()

            self.rdCount += 1
            time.sleep(wait)
            timestamp(f"< {self.val} >", "r", idx, i)
            self.rdCount -= 1

            time.sleep(end)

    def writter(self, idx, start, wait, end, repeat, data):
        time.sleep(start)
        timestamp("started", "w", idx)
        for i in range(repeat):
            waitOne = 0
            while self.rdCount > 0:
                if waitOne:
                    waitOne = 1
                    timestamp(f"waiting", "w", idx, i)
                self.wait()

            self.rdCount -= 1
            time.sleep(wait)
            self.val = data
            timestamp(f"< {self.val} >", "w", idx, i)
            self.rdCount += 1

            time.sleep(end)


def linput(data):
    return list(map(int, input(data).split()))


def iinput(data):
    return int(input(data))


readers = iinput("Number of readers : ")
readerStart = linput("Reader start time : ")
readerWait = linput("Reader Wait time : ")
readerEnd = linput("Reader End time : ")
readerRepeat = linput("Reader Repeats : ")
writters = iinput("Number of writters : ")
writerData = linput("Writter data : ")
writterStart = linput("Writter start time : ")
writterWait = linput("Writter wait time : ")
wriiterEnd = linput("Writter end time : ")
writterRepeat = linput("Writter repeats : ")

start = time.perf_counter_ns()
atexit.register(exit_handler, start=start)
print()

problem = Problem(
    readers,
    readerStart,
    readerWait,
    readerEnd,
    readerRepeat,
    writters,
    writerData,
    writterStart,
    writterWait,
    wriiterEnd,
    writterRepeat,
)