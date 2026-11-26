class Solution:
    def minimumSubarrayLength(self, nums: List[int], k: int) -> int:
        n = len(nums)
        counts = [0] * 30
        cur_or = 0
        ans = n + 1
        left = 0
        for right, x in enumerate(nums):
            cur_or |= x
            v = x
            while v:
                lb = v & -v
                counts[lb.bit_length() - 1] += 1
                v ^= lb
            while left <= right and cur_or >= k:
                length = right - left + 1
                if length < ans:
                    ans = length
                y = nums[left]
                left += 1
                while y:
                    lb = y & -y
                    b = lb.bit_length() - 1
                    counts[b] -= 1
                    if counts[b] == 0:
                        cur_or ^= lb
                    y ^= lb
        return -1 if ans > n else ans
