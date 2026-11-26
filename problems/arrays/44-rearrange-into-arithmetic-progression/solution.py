class Solution:
    def canRearrangeArithmeticProgression(self, nums: List[int]) -> bool:
        ordered = sorted(nums)
        step = ordered[1] - ordered[0]
        return all(ordered[i] - ordered[i - 1] == step for i in range(2, len(ordered)))
