class HitCounter:
    def __init__(self):
        self.q = deque()
        self.total = 0

    def _evict(self, timestamp: int) -> None:
        cutoff = timestamp - 300
        while self.q and self.q[0][0] <= cutoff:
            self.total -= self.q.popleft()[1]

    def hit(self, timestamp: int) -> None:
        self._evict(timestamp)
        if self.q and self.q[-1][0] == timestamp:
            self.q[-1][1] += 1
        else:
            self.q.append([timestamp, 1])
        self.total += 1

    def getHits(self, timestamp: int) -> int:
        self._evict(timestamp)
        return self.total
