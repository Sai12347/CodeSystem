class Solution:
    def countSubarraysWithXor(self, nums: List[int], k: int) -> int:
        freq = {0: 1}
        pref = 0
        ans = 0
        for x in nums:
            pref ^= x
            ans += freq.get(pref ^ k, 0)
            freq[pref] = freq.get(pref, 0) + 1
        return ans
