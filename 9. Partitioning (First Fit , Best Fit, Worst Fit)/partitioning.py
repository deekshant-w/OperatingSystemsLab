from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


class Block:
    def __init__(self, size, available, usable):
        """
        size -> total size of block
        usable -> remaining usable space in block
        available -> if the block can be used
        """
        self.size = size
        self.available = available
        self.usable = usable

    def __repr__(self) -> str:
        return f"({self.size=}, {self.available=}, {self.usable=})"


class RAM:
    def __init__(self, size, usable, processes):
        self.blocks = [Block(size[x], usable[x], size[x]) for x in range(len(size))]
        self.processes = processes
        self.positioning = [[] for _ in range(len(size))]
        self.fail = []
        self.run()
        self.output()

    def run(self):
        ...

    def output(self):
        table = Table(show_header=False, box=box.SQUARE, show_lines=True)
        table.add_row(
            *[
                " | ".join([f"P{y[0]+1}:{y[1]}MB" for y in x]) if x else " X "
                for x in self.positioning
            ]
        )
        table.add_row(*[str(x.size) for x in self.blocks])
        console.print(table)
        print("\n")
        # print(self.fail)


class FF(RAM):
    def __init__(self, size, usable, processes):
        super().__init__(size, usable, processes)

    def run(self):
        for ip, p in enumerate(self.processes):
            for ib, b in enumerate(self.blocks):
                if b.available and b.usable >= p:
                    self.positioning[ib].append((ip, p))
                    self.blocks[ib].usable -= p
                    break
            else:
                self.fail.append((ip, p))
        print("\nFirst Fit")


class BF(RAM):
    def __init__(self, size, usable, processes):
        super().__init__(size, usable, processes)

    def run(self):
        for ip, p in enumerate(self.processes):
            minIdx = None
            for ib, b in enumerate(self.blocks):
                if (
                    b.available
                    and b.usable >= p
                    and (
                        minIdx is None
                        or (
                            self.blocks[minIdx].usable - p > b.usable - p
                            and b.usable - p >= 0
                        )
                    )
                ):
                    minIdx = ib
            if minIdx:
                self.positioning[minIdx].append((ip, p))
                self.blocks[minIdx].usable -= p
            else:
                self.fail.append((ip, p))

        print("\nBest Fit")


class WF(RAM):
    def __init__(self, size, usable, processes):
        super().__init__(size, usable, processes)

    def run(self):
        for ip, p in enumerate(self.processes):
            maxidx = None
            for ib, b in enumerate(self.blocks):
                if (
                    b.available
                    and b.usable >= p
                    and (
                        maxidx is None
                        or (
                            self.blocks[maxidx].usable - p < b.usable - p
                            and b.usable - p >= 0
                        )
                    )
                ):
                    maxidx = ib
            if maxidx:
                self.positioning[maxidx].append((ip, p))
                self.blocks[maxidx].usable -= p
            else:
                self.fail.append((ip, p))
        print("\nWorst Fit")


size = list(map(int, input("Ram block sizes: ").split()))
usable = list(map(int, input(f"Block usable[{len(size)}] (0/1): ").split()))
processes = list(map(int, input("Processes sizes: ").split()))

print("Deekshant Wadhwa\n01296303118")

FF(size, usable, processes)
BF(size, usable, processes)
WF(size, usable, processes)
