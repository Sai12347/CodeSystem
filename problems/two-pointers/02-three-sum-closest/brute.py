class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        n = len(nums)
        best = nums[0] + nums[1] + nums[2]
        best_diff = abs(best - target)
        for i in range(n - 2):
            a = nums[i]
            for j in range(i + 1, n - 1):
                ab = a + nums[j]
                for k in range(j + 1, n):
                    s = ab + nums[k]
                    d = abs(s - target)
                    if d < best_diff:
                        best_diff = d
                        best = s
        return best
