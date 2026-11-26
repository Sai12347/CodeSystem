class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        uniq = sorted(set(nums))
        for i, v in enumerate(uniq):
            nums[i] = v
        return len(uniq)
