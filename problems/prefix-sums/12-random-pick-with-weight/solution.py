import bisect
import random


class Solution:
    def __init__(self, w: List[int]):
        self.prefix = []
        running = 0
        for weight in w:
            running += weight
            self.prefix.append(running)
        self.total = running

    def pickIndex(self) -> int:
        target = random.randint(1, self.total)
        return bisect.bisect_left(self.prefix, target)
