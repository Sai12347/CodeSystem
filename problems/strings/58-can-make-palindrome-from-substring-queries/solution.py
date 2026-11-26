class Solution:
    def canMakePaliQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        pref = [0] * (n + 1)
        for i, ch in enumerate(s):
            pref[i + 1] = pref[i] ^ (1 << (ord(ch) - 97))
        return [(pref[r + 1] ^ pref[l]).bit_count() // 2 <= k for l, r, k in queries]
