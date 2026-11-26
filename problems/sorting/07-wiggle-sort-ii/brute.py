class Solution:
    def wiggleSort(self, nums: List[int]) -> None:
        n = len(nums)
        s = sorted(nums)
        mid = (n + 1) // 2
        nums[0::2] = s[:mid][::-1]
        nums[1::2] = s[mid:][::-1]
