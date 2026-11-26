class KStacks:
    def __init__(self, k: int, capacity: int):
        self.data = [0] * capacity
        self.nxt = list(range(1, capacity)) + [-1]
        self.top = [-1] * k
        self.sizes = [0] * k
        self.free_head = 0

    def push(self, stackId: int, val: int) -> bool:
        if self.free_head == -1:
            return False
        slot = self.free_head
        self.free_head = self.nxt[slot]
        self.data[slot] = val
        self.nxt[slot] = self.top[stackId]
        self.top[stackId] = slot
        self.sizes[stackId] += 1
        return True

    def pop(self, stackId: int) -> int:
        slot = self.top[stackId]
        if slot == -1:
            return -1
        self.top[stackId] = self.nxt[slot]
        self.nxt[slot] = self.free_head
        self.free_head = slot
        self.sizes[stackId] -= 1
        return self.data[slot]

    def peek(self, stackId: int) -> int:
        slot = self.top[stackId]
        return -1 if slot == -1 else self.data[slot]

    def size(self, stackId: int) -> int:
        return self.sizes[stackId]
