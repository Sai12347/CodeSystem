class Solution:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        counts = [0] * k
        counts[0] = 1
        prefix = 0
        ans = 0
        for x in nums:
            prefix = (prefix + x) % k
            ans += counts[prefix]
            counts[prefix] += 1
        return ans
