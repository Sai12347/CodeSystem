class Solution:
    def countTotalSetBits(self, n: int) -> int:
        m = n + 1
        total = 0
        half = 1
        while half <= n:
            cycle = half << 1
            total += (m // cycle) * half
            rem = m % cycle
            if rem > half:
                total += rem - half
            half = cycle
        return total
