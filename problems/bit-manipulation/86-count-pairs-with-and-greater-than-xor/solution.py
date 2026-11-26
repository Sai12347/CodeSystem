class Solution:
    def countAndGreaterThanXor(self, nums: List[int]) -> int:
        buckets = [0] * 31
        for x in nums:
            buckets[x.bit_length() - 1] += 1
        ans = 0
        for c in buckets:
            ans += c * (c - 1) // 2
        return ans
