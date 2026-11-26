class Solution:
    def wonderfulSubstrings(self, word: str) -> int:
        cnt = [0] * 1024
        cnt[0] = 1
        mask = 0
        ans = 0
        for ch in word:
            mask ^= 1 << (ord(ch) - 97)
            ans += cnt[mask]
            for b in range(10):
                ans += cnt[mask ^ (1 << b)]
            cnt[mask] += 1
        return ans
