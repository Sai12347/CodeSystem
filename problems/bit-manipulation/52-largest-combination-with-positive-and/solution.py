class Solution:
    def largestCombination(self, candidates: List[int]) -> int:
        best = 0
        for b in range(24):
            mask = 1 << b
            cnt = 0
            for x in candidates:
                if x & mask:
                    cnt += 1
            if cnt > best:
                best = cnt
        return best
