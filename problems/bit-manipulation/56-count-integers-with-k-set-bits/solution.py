class Solution:
    def countWithKSetBits(self, n: int, k: int) -> int:
        if k == 0:
            return 1
        MAX_B = 60
        comb = [[0] * (MAX_B + 1) for _ in range(MAX_B + 1)]
        for i in range(MAX_B + 1):
            comb[i][0] = 1
            for j in range(1, i + 1):
                comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j]
        ans = 0
        rem = k
        for b in range(MAX_B - 1, -1, -1):
            if (n >> b) & 1:
                if 0 <= rem <= b:
                    ans += comb[b][rem]
                rem -= 1
                if rem < 0:
                    break
        if rem == 0:
            ans += 1
        return ans
