class MyCircularQueue:
    def __init__(self, k: int):
        self.buf = [0] * k
        self.cap = k
        self.head = 0
        self.count = 0

    def enQueue(self, value: int) -> bool:
        if self.count == self.cap:
            return False
        self.buf[(self.head + self.count) % self.cap] = value
        self.count += 1
        return True

    def deQueue(self) -> bool:
        if self.count == 0:
            return False
        self.head = (self.head + 1) % self.cap
        self.count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.count == 0 else self.buf[self.head]

    def Rear(self) -> int:
        return -1 if self.count == 0 else self.buf[(self.head + self.count - 1) % self.cap]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == self.cap
