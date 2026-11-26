class Solution:
    def countIncreasingSubarrays(self, nums: List[int]) -> int:
        run = answer = 0
        for i, x in enumerate(nums):
            run = run + 1 if i > 0 and x > nums[i - 1] else 1
            answer += run
        return answer
