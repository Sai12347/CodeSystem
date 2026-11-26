import random


class Solution:
    def __init__(self, w: List[int]):
        self.w = list(w)
        self.total = sum(w)

    def pickIndex(self) -> int:
        target = random.randint(1, self.total)
        acc = 0
        for i, weight in enumerate(self.w):
            acc += weight
            if acc >= target:
                return i
        return len(self.w) - 1
