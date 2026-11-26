class Solution:
    def find132pattern(self, nums: List[int]) -> bool:
        n = len(nums)
        if n < 3:
            return False
        min_left = nums[0]
        for j in range(1, n - 1):
            nj = nums[j]
            if min_left < nj:
                for k in range(j + 1, n):
                    if min_left < nums[k] < nj:
                        return True
            if nj < min_left:
                min_left = nj
        return False
