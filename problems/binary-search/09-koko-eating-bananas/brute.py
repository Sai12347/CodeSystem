class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        hi = max(piles)
        if hi <= 5000:
            for k in range(1, hi + 1):
                if sum(math.ceil(p / k) for p in piles) <= h:
                    return k
            return hi
        lo = 1
        while lo < hi:
            mid = (lo + hi) // 2
            if sum((p - 1) // mid + 1 for p in piles) <= h:
                hi = mid
            else:
                lo = mid + 1
        return lo
