class MyCircularDeque:
    def __init__(self, k: int):
        self.cap = k
        self.dq = deque()

    def insertFront(self, value: int) -> bool:
        if len(self.dq) == self.cap:
            return False
        self.dq.appendleft(value)
        return True

    def insertLast(self, value: int) -> bool:
        if len(self.dq) == self.cap:
            return False
        self.dq.append(value)
        return True

    def deleteFront(self) -> bool:
        if not self.dq:
            return False
        self.dq.popleft()
        return True

    def deleteLast(self) -> bool:
        if not self.dq:
            return False
        self.dq.pop()
        return True

    def getFront(self) -> int:
        return self.dq[0] if self.dq else -1

    def getRear(self) -> int:
        return self.dq[-1] if self.dq else -1

    def isEmpty(self) -> bool:
        return len(self.dq) == 0

    def isFull(self) -> bool:
        return len(self.dq) == self.cap
