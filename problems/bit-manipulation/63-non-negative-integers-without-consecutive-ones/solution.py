class Solution:
    def findIntegers(self, n: int) -> int:
        fib = [0] * 32
        fib[0] = 1
        fib[1] = 2
        for i in range(2, 32):
            fib[i] = fib[i - 1] + fib[i - 2]
        ans = 0
        prev_bit = 0
        for b in range(30, -1, -1):
            if (n >> b) & 1:
                ans += fib[b]
                if prev_bit == 1:
                    return ans
                prev_bit = 1
            else:
                prev_bit = 0
        return ans + 1
