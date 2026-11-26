class Solution:
    def countPalindromicSubsequence(self, s: str) -> int:
        first = [-1] * 26
        last = [-1] * 26
        for i, ch in enumerate(s):
            idx = ord(ch) - 97
            if first[idx] == -1:
                first[idx] = i
            last[idx] = i
        ans = 0
        for c in range(26):
            if first[c] != -1 and first[c] + 1 < last[c]:
                seen = 0
                for i in range(first[c] + 1, last[c]):
                    seen |= 1 << (ord(s[i]) - 97)
                ans += seen.bit_count()
        return ans
