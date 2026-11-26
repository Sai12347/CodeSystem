class Solution:
    def numOfWindowsAboveThreshold(self, nums: List[int], k: int, threshold: int) -> int:
        target = k * threshold
        total = sum(nums[:k])
        answer = int(total >= target)
        for i in range(k, len(nums)):
            total += nums[i] - nums[i - k]
            answer += total >= target
        return answer
