class Solution:
    def fibonacciMod(self, n: int) -> int:
        MOD = 1_000_000_007

        def fib(k: int) -> tuple[int, int]:
            if k == 0:
                return (0, 1)
            a, b = fib(k >> 1)
            c = a * ((2 * b - a) % MOD) % MOD
            d = (a * a + b * b) % MOD
            if k & 1:
                return (d, (c + d) % MOD)
            return (c, d)

        return fib(n)[0]
