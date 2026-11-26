class Solution:
    def countSubarraysWithFixedBounds(self, nums: List[int], minK: int, maxK: int) -> int:
        last_bad = last_min = last_max = -1
        answer = 0
        for i, x in enumerate(nums):
            if x < minK or x > maxK: last_bad = i
            if x == minK: last_min = i
            if x == maxK: last_max = i
            answer += max(0, min(last_min, last_max) - last_bad)
        return answer
