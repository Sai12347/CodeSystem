import heapq

class DinnerPlates:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.stacks = []
        self.avail = []

    def push(self, val: int) -> None:
        while self.avail and (self.avail[0] >= len(self.stacks) or len(self.stacks[self.avail[0]]) == self.cap):
            heapq.heappop(self.avail)
        if self.avail:
            idx = self.avail[0]
            self.stacks[idx].append(val)
            if len(self.stacks[idx]) == self.cap:
                heapq.heappop(self.avail)
        else:
            self.stacks.append([val])
            if self.cap > 1:
                heapq.heappush(self.avail, len(self.stacks) - 1)

    def pop(self) -> int:
        while self.stacks and not self.stacks[-1]:
            self.stacks.pop()
        if not self.stacks:
            return -1
        idx = len(self.stacks) - 1
        val = self.stacks[idx].pop()
        while self.stacks and not self.stacks[-1]:
            self.stacks.pop()
        if idx < len(self.stacks):
            heapq.heappush(self.avail, idx)
        return val

    def popAtStack(self, index: int) -> int:
        if index < 0 or index >= len(self.stacks) or not self.stacks[index]:
            return -1
        val = self.stacks[index].pop()
        while self.stacks and not self.stacks[-1]:
            self.stacks.pop()
        if index < len(self.stacks):
            heapq.heappush(self.avail, index)
        return val
