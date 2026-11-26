class Solution:
    def countSubarraysWithMaximum(self, nums: List[int]) -> int:
        maximum = max(nums)
        run = answer = 0
        for x in nums:
            run = run + 1 if x == maximum else 0
            answer += run
        return answer
