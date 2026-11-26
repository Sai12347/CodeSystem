class Solution:
    def subarraysWithKDistinct(self, nums: List[int], k: int) -> int:
        def at_most(limit: int) -> int:
            if limit <= 0:
                return 0
            counts = defaultdict(int)
            left = 0
            total = 0
            for right, val in enumerate(nums):
                counts[val] += 1
                while len(counts) > limit:
                    left_val = nums[left]
                    counts[left_val] -= 1
                    if counts[left_val] == 0:
                        del counts[left_val]
                    left += 1
                total += right - left + 1
            return total

        return at_most(k) - at_most(k - 1)
