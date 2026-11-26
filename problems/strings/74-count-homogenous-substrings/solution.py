class Solution:
    def countHomogenous(self, s: str) -> int:
        mod = 1000000007
        ans = 0
        run = 0
        prev = ""
        for ch in s:
            if ch == prev:
                run += 1
            else:
                run = 1
                prev = ch
            ans = (ans + run) % mod
        return ans
