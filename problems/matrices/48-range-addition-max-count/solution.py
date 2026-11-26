class Solution:
    def maxCount(self, m: int, n: int, ops: List[List[int]]) -> int:
        min_r, min_c = m, n
        for a, b in ops:
            if a < min_r:
                min_r = a
            if b < min_c:
                min_c = b
        return min_r * min_c
