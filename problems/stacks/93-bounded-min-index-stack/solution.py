class BoundedMinStack:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.vals = []
        self.mins = []
        self.min_idx = []

    def push(self, val: int) -> bool:
        if len(self.vals) == self.cap:
            return False
        idx = len(self.vals)
        self.vals.append(val)
        if idx == 0 or val < self.mins[-1]:
            self.mins.append(val)
            self.min_idx.append(idx)
        else:
            self.mins.append(self.mins[-1])
            self.min_idx.append(self.min_idx[-1])
        return True

    def pop(self) -> int:
        if not self.vals:
            return -1
        self.mins.pop()
        self.min_idx.pop()
        return self.vals.pop()

    def top(self) -> int:
        return self.vals[-1] if self.vals else -1

    def getMin(self) -> int:
        return self.mins[-1] if self.mins else -1

    def getMinIndex(self) -> int:
        return self.min_idx[-1] if self.min_idx else -1
