class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 18:
            def dfs(i: int) -> int:
                if i >= n:
                    return 0
                return max(dfs(i + 1), nums[i] + dfs(i + 2))
            return dfs(0)

        # Independent two-state DP tracking (robbed_prev, skipped_prev)
        take = 0
        skip = 0
        for x in nums:
            take, skip = skip + x, max(skip, take)
        return max(take, skip)
