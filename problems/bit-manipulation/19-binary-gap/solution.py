class Solution:
    def binaryGap(self, n: int) -> int:
        last = -1
        best = 0
        pos = 0
        while n > 0:
            if n & 1:
                if last != -1 and pos - last > best:
                    best = pos - last
                last = pos
            n >>= 1
            pos += 1
        return best
