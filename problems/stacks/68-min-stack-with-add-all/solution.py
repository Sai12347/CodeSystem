class OffsetMinStack:
    def __init__(self):
        self.st = []
        self.offset = 0

    def push(self, val: int) -> None:
        adj = val - self.offset
        mn = adj if not self.st or adj < self.st[-1][1] else self.st[-1][1]
        self.st.append((adj, mn))

    def pop(self) -> None:
        self.st.pop()

    def addAll(self, delta: int) -> None:
        self.offset += delta

    def top(self) -> int:
        return self.st[-1][0] + self.offset

    def getMin(self) -> int:
        return self.st[-1][1] + self.offset
