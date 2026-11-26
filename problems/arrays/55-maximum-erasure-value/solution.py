class Solution:
    def maximumUniqueSubarray(self, nums: List[int]) -> int:
        left = total = best = 0
        seen = set()
        for x in nums:
            while x in seen:
                seen.remove(nums[left]); total -= nums[left]; left += 1
            seen.add(x); total += x
            best = max(best, total)
        return best
