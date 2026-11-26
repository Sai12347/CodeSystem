from collections import deque
import math


class MRUQueue:
    def __init__(self, n: int):
        self.block = max(1, math.isqrt(n))
        self.buckets: list[deque[int]] = []
        for start in range(1, n + 1, self.block):
            end = min(n + 1, start + self.block)
            self.buckets.append(deque(range(start, end)))

    def fetch(self, k: int) -> int:
        b = (k - 1) // self.block
        off = (k - 1) % self.block
        bucket = self.buckets[b]
        bucket.rotate(-off)
        val = bucket.popleft()
        bucket.rotate(off)
        for j in range(b, len(self.buckets) - 1):
            self.buckets[j].append(self.buckets[j + 1].popleft())
        self.buckets[-1].append(val)
        return val
