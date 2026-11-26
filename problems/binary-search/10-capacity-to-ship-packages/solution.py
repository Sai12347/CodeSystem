class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        left, right = max(weights), sum(weights)
        while left < right:
            mid = left + (right - left) // 2
            needed = 1
            load = 0
            for w in weights:
                if load + w > mid:
                    needed += 1
                    load = w
                else:
                    load += w
            if needed <= days:
                right = mid
            else:
                left = mid + 1
        return left
