class Solution:
    def maxDistToClosest(self, seats: List[int]) -> int:
        last = -1
        best = 0
        for i, occupied in enumerate(seats):
            if occupied:
                best = max(best, i if last == -1 else (i - last) // 2)
                last = i
        return max(best, len(seats) - 1 - last)
