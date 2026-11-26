class Logger:
    def __init__(self):
        self.q = deque()
        self.active = set()

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        cutoff = timestamp - 10
        while self.q and self.q[0][0] <= cutoff:
            _, old_msg = self.q.popleft()
            self.active.remove(old_msg)
        if message in self.active:
            return False
        self.active.add(message)
        self.q.append((timestamp, message))
        return True
