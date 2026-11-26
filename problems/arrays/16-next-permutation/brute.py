class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)
        pivot = -1
        for i in range(n - 2, -1, -1):
            if nums[i] < nums[i + 1]:
                pivot = i
                break
        if pivot == -1:
            nums.sort()
            return
        best_j = -1
        for j in range(pivot + 1, n):
            if nums[j] > nums[pivot]:
                if best_j == -1 or nums[j] <= nums[best_j]:
                    best_j = j
        nums[pivot], nums[best_j] = nums[best_j], nums[pivot]
        nums[pivot + 1:] = sorted(nums[pivot + 1:])
