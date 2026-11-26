class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        found = set()
        n = len(nums)
        for i in range(n):
            target = -nums[i]
            seen = set()
            for j in range(i + 1, n):
                need = target - nums[j]
                if need in seen:
                    found.add(tuple(sorted((nums[i], nums[j], need))))
                seen.add(nums[j])
        return [list(t) for t in found]
