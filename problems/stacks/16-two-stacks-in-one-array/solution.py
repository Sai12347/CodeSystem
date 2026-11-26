class TwoStacks:
    def __init__(self, capacity: int):
        self.arr = [0] * capacity
        self.cap = capacity
        self.top1 = -1
        self.top2 = capacity

    def push1(self, val: int) -> bool:
        if self.top1 + 1 == self.top2:
            return False
        self.top1 += 1
        self.arr[self.top1] = val
        return True

    def push2(self, val: int) -> bool:
        if self.top1 + 1 == self.top2:
            return False
        self.top2 -= 1
        self.arr[self.top2] = val
        return True

    def pop1(self) -> int:
        if self.top1 == -1:
            return -1
        val = self.arr[self.top1]
        self.top1 -= 1
        return val

    def pop2(self) -> int:
        if self.top2 == self.cap:
            return -1
        val = self.arr[self.top2]
        self.top2 += 1
        return val

    def size1(self) -> int:
        return self.top1 + 1

    def size2(self) -> int:
        return self.cap - self.top2
