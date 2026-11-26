class Solution:
    def maxMinDistance(self, stalls: List[int], cows: int) -> int:
        stalls.sort()
        lo, hi = 1, stalls[-1] - stalls[0]
        while lo < hi:
            mid = lo + (hi - lo + 1) // 2
            placed = 1
            last = stalls[0]
            for pos in stalls[1:]:
                if pos - last >= mid:
                    placed += 1
                    last = pos
                    if placed == cows:
                        break
            if placed >= cows:
                lo = mid
            else:
                hi = mid - 1
        return lo
