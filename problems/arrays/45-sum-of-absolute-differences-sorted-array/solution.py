class Solution:
    def getAbsoluteDifferences(self, nums: List[int]) -> List[int]:
        total = sum(nums)
        left = 0
        answer = []
        n = len(nums)
        for i, x in enumerate(nums):
            answer.append(x * i - left + total - left - x * (n - i))
            left += x
        return answer
