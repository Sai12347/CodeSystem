class Solution:
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        n = len(customers)
        base = sum(c for c, g in zip(customers, grumpy) if g == 0)
        best_extra = 0
        for i in range(n - minutes + 1):
            extra = sum(customers[j] for j in range(i, i + minutes) if grumpy[j] == 1)
            if extra > best_extra:
                best_extra = extra
        return base + best_extra
