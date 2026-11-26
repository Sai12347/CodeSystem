class Solution:
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        n = len(customers)
        base = 0
        extra = 0
        for i in range(minutes):
            if grumpy[i] == 0:
                base += customers[i]
            else:
                extra += customers[i]

        best_extra = extra
        for i in range(minutes, n):
            if grumpy[i] == 0:
                base += customers[i]
            else:
                extra += customers[i]
            if grumpy[i - minutes] == 1:
                extra -= customers[i - minutes]
            if extra > best_extra:
                best_extra = extra

        return base + best_extra
