from collections import deque
import heapq


class LRUKCache:
    def __init__(self, capacity: int, k: int):
        self.cap = capacity
        self.k = k
        self.tick = 0
        self.seq = 0
        self.vals: dict[int, int] = {}
        self.hist: dict[int, deque[int]] = {}
        self.ver: dict[int, int] = {}
        self.heap: list[tuple[int, int, int, int]] = []

    def _record_access(self, key: int) -> None:
        self.tick += 1
        dq = self.hist[key]
        dq.append(self.tick)
        if len(dq) > self.k:
            dq.popleft()
        self.seq += 1
        self.ver[key] = self.seq
        tier = 0 if len(dq) < self.k else 1
        heapq.heappush(self.heap, (tier, dq[0], self.seq, key))

    def get(self, key: int) -> int:
        if key not in self.vals:
            return -1
        self._record_access(key)
        return self.vals[key]

    def put(self, key: int, value: int) -> None:
        if key in self.vals:
            self.vals[key] = value
            self._record_access(key)
            return
        if len(self.vals) == self.cap:
            while self.heap:
                _, _, v, cand = heapq.heappop(self.heap)
                if cand in self.vals and self.ver[cand] == v:
                    del self.vals[cand]
                    del self.hist[cand]
                    del self.ver[cand]
                    break
        self.vals[key] = value
        self.hist[key] = deque()
        self._record_access(key)
