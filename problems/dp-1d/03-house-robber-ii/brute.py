class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
        if n <= 18:
            def dfs(i: int, took_first: bool) -> int:
                if i >= n:
                    return 0
                best = dfs(i + 1, took_first)
                if not (i == n - 1 and took_first):
                    best = max(best, nums[i] + dfs(i + 2, took_first or i == 0))
                return best
            return dfs(0, False)

        # Independent explicit state machine: track (took_prev, skipped_prev) for both cases
        # Case A: forced take house 0
        take_a, skip_a = nums[0], -10**18
        for i in range(1, n - 1):
            take_a, skip_a = skip_a + nums[i], max(skip_a, take_a)
        best_a = max(take_a, skip_a)

        # Case B: forced skip house 0
        take_b, skip_b = -10**18, 0
        for i in range(1, n):
            take_b, skip_b = skip_b + nums[i], max(skip_b, take_b)
        best_b = max(take_b, skip_b)

        return max(best_a, best_b)
