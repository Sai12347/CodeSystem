class Solution:
    def climbStairs(self, n: int) -> int:
        # Independent combinatorial count: choose k two-step moves out of (n - k) total moves.
        total = 0
        for twos in range(n // 2 + 1):
            total += math.comb(n - twos, twos)
        return total
