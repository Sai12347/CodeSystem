from itertools import groupby


class Solution:
    def countAndSay(self, n: int) -> str:
        if n == 1:
            return "1"
        prev = self.countAndSay(n - 1)
        return "".join(f"{sum(1 for _ in g)}{ch}" for ch, g in groupby(prev))
