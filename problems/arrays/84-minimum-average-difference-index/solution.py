class Solution:
    def minimumAverageDifference(self, nums: List[int]) -> int:
        total = sum(nums)
        left = 0
        best, answer = None, 0
        n = len(nums)
        for i, x in enumerate(nums):
            left += x
            left_avg = left // (i + 1)
            right_avg = (total - left) // (n - i - 1) if i + 1 < n else 0
            diff = abs(left_avg - right_avg)
            if best is None or diff < best: best, answer = diff, i
        return answer
