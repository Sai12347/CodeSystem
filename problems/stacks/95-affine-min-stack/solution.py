class AffineMinStack:
    def __init__(self):
        self.vals = []
        self.mins = []
        self.maxs = []
        self.sign = 1
        self.offset = 0

    def push(self, val: int) -> None:
        stored = self.sign * (val - self.offset)
        self.vals.append(stored)
        if not self.mins:
            self.mins.append(stored)
            self.maxs.append(stored)
        else:
            self.mins.append(stored if stored < self.mins[-1] else self.mins[-1])
            self.maxs.append(stored if stored > self.maxs[-1] else self.maxs[-1])

    def pop(self) -> None:
        self.vals.pop()
        self.mins.pop()
        self.maxs.pop()

    def addAll(self, delta: int) -> None:
        self.offset += delta

    def negateAll(self) -> None:
        self.sign = -self.sign
        self.offset = -self.offset

    def top(self) -> int:
        return self.sign * self.vals[-1] + self.offset

    def getMin(self) -> int:
        if self.sign == 1:
            return self.mins[-1] + self.offset
        return -self.maxs[-1] + self.offset
