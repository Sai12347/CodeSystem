class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n
        if k:
            nums[:] = nums[-k:] + nums[:-k]
