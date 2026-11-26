class Solution:
    def minOpsToZero(self, n: int) -> int:
        x = n
        ops = 0
        while x > 0:
            low = x & -x
            if x & (low << 1):
                x += low
            else:
                x -= low
            ops += 1
        return ops
