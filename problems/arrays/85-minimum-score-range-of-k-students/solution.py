class Solution:
    def minimumScoreRange(self, nums: List[int], k: int) -> int:
        a = sorted(nums)
        return min(a[i + k - 1] - a[i] for i in range(len(a) - k + 1))
