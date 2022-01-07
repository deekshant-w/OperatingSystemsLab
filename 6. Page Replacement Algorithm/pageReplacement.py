# Abstract Classes
from abc import ABCMeta, abstractmethod

# Copy lists
from copy import deepcopy
from operator import le

# Output
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich import box


def me():
    print("\n")
    console = Console(width=20)
    console.print(
        "Deekshant Wadhwa\nIT-EVE\n[not bold white]01296303118",
        style="white on dark_blue",
        justify="center",
    )


class PageReplacement(metaclass=ABCMeta):
    def __init__(self, size, pages, name):
        self.size = size
        self.pages = pages
        self.name = name

        self.hits = 0
        self.miss = 0

        # records hit or miss
        self.record = []

        # records buffer history
        self.history = []

        # Execute
        self.process()
        self.output()

    # Page Replacement Stratergy
    @abstractmethod
    def stratergy(self, page):
        ...

    def newPage(self, i, page):
        ...

    def Hit(self):
        self.hits += 1
        self.record.append("Hit")

    def Miss(self):
        self.miss += 1
        self.record.append("Miss")

    def process(self):
        for i, page in enumerate(self.pages):
            # individual processing of all pages
            self.newPage(i, page)

            # first page
            if not self.history:
                self.Miss()
                self.history.append([page])
                continue

            ## further pages -

            # page found in buffer
            if page in self.history[-1]:
                self.Hit()
                self.history.append(deepcopy(self.history[-1]))

            # page not found in buffer
            else:
                self.Miss()

                # space available in buffer
                if len(self.history[-1]) < self.size:
                    newBuffer = deepcopy(self.history[-1])
                    newBuffer.append(page)

                # buffer is full
                else:
                    newBuffer = self.stratergy(page)

                self.history.append(newBuffer)

    def output(self):
        # Cleaning Data
        for i, h in enumerate(self.history):
            if len(h) < self.size:
                self.history[i] = h + [" "] * (self.size - len(h))
            self.history[i] = list(reversed(self.history[i]))

        # Making Output
        console = Console()
        console.print(f"\n\n {self.name} ", style="black on white")
        table = Table(show_header=True, show_footer=True, box=box.SQUARE)

        # Table Formatting
        miss_footer_style = Style(bold=False, color="red1")
        hit_footer_style = Style(bold=False, color="chartreuse1")
        empty_footer_style = Style(bold=False, color="grey93")
        cell_style = "yellow1"
        header_style = Style(bold=True, color="cyan1")

        # Adding columns
        table.add_column(
            header="", 
            footer="Empty", 
            justify="center", 
            footer_style=empty_footer_style
        )
        for i in range(len(self.history)):
            footer_style = hit_footer_style if self.record[i] == "Hit" else miss_footer_style
            table.add_column(
                header=str(pages[i]),
                footer=self.record[i],
                justify="center",
                width=5,
                header_style=header_style,
                footer_style=footer_style,
                style=cell_style,
            )

        # Adding rows
        for i in range(len(self.history[0])):
            row = [""]
            for j in range(len(self.history)):
                row.append(str(self.history[j][i]))
            table.add_row(*row)

        console.print(table)
        console.print(f"[green]Hits: {str(self.hits)}")
        console.print(f"[red]Miss: {str(self.miss)}")


class FIFO(PageReplacement):
    # page not in buffer, and buffer is full
    def stratergy(self, page):
        prev = deepcopy(self.history[-1])
        prev.pop(0)
        prev.append(page)
        return prev

    def __init__(self, size, pages):
        name = "First In First Out (FIFO)"
        super().__init__(size, pages, name)


class LRU(PageReplacement):
    # page not in buffer, and buffer is full
    def stratergy(self, page):
        prev = deepcopy(self.history[-1])

        # page which was accessed earliest
        removePage = min(prev, key=self.accessMapping.get)

        # replacing old page with new pageS
        prev = [page if x == removePage else x for x in prev]
        return prev

    def __init__(self, size, pages):
        # map access times
        self.accessMapping = {}
        name = "Least Recently Used (LRU)"
        super().__init__(size, pages, name)

    def newPage(self, i, page):
        self.accessMapping[page] = i


class Optimal(PageReplacement):
    def stratergy(self, page):
        prev = deepcopy(self.history[-1])

        # checking future pages
        pages: list = deepcopy(self.history[-1])
        for i in range(self.currentPage, len(self.pages)):
            if len(pages) == 1:
                break
            curr = self.pages[i]
            if curr in pages:
                pages.remove(curr)

        # replace page
        prev = [page if x == pages[0] else x for x in prev]
        return prev

    def __init__(self, size, pages):
        self.currentPage = -1
        name = "Optimal Page replacement"
        super().__init__(size, pages, name)

    def newPage(self, i, page):
        self.currentPage = i

#Inputs
size = int(input("Size: "))
pages = list(map(int, input("Frames: ").split()))
me()

# Page replacement algorithms
fifo = FIFO(size, pages)
lru = LRU(size, pages)
opt = Optimal(size, pages)

me()
print("\n")