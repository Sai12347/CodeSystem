class Solution:
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        total = sum(nums)
        if total % k != 0:
            return False
        target = total // k
        if max(nums) > target:
            return False

        n = len(nums)
        dp = [-1] * (1 << n)
        dp[0] = 0
        for mask in range(1 << n):
            cur = dp[mask]
            if cur == -1:
                continue
            rem = target - cur
            for i in range(n):
                if not (mask & (1 << i)) and nums[i] <= rem:
                    nmask = mask | (1 << i)
                    if dp[nmask] == -1:
                        nxt = cur + nums[i]
                        dp[nmask] = 0 if nxt == target else nxt
        return dp[(1 << n) - 1] == 0
