class Solution:
    def findOriginalPrefixXor(self, pref: List[int]) -> List[int]:
        n = len(pref)
        ans = [pref[0]] * n
        for i in range(1, n):
            ans[i] = pref[i] ^ pref[i - 1]
        return ans
