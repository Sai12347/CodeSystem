class MyCircularQueue:
    def __init__(self, k: int):
        self.cap = k
        self.q = deque()

    def enQueue(self, value: int) -> bool:
        if len(self.q) == self.cap:
            return False
        self.q.append(value)
        return True

    def deQueue(self) -> bool:
        if not self.q:
            return False
        self.q.popleft()
        return True

    def Front(self) -> int:
        return self.q[0] if self.q else -1

    def Rear(self) -> int:
        return self.q[-1] if self.q else -1

    def isEmpty(self) -> bool:
        return len(self.q) == 0

    def isFull(self) -> bool:
        return len(self.q) == self.cap
