class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        def can_ship(cap: int) -> bool:
            used = 1
            cur = 0
            for w in weights:
                if cur + w > cap:
                    used += 1
                    cur = w
                else:
                    cur += w
            return used <= days

        lo, hi = max(weights), sum(weights)
        if hi - lo <= 5000:
            for cap in range(lo, hi + 1):
                if can_ship(cap):
                    return cap
            return hi
        while lo < hi:
            mid = (lo + hi) // 2
            if can_ship(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
