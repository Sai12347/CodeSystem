class Solution:
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        total = sum(nums)
        if total % k != 0:
            return False
        target = total // k
        nums.sort(reverse=True)
        if nums[0] > target:
            return False
        if k == 1:
            return True

        n = len(nums)
        full = (1 << n) - 1
        failed = bytearray(1 << n)

        def dfs(mask: int, cur_sum: int) -> bool:
            if mask == full:
                return True
            if failed[mask]:
                return False

            if cur_sum == 0:
                for i in range(n):
                    if not (mask & (1 << i)):
                        nxt = nums[i]
                        if dfs(mask | (1 << i), 0 if nxt == target else nxt):
                            return True
                        break
            else:
                for i in range(n):
                    if mask & (1 << i):
                        continue
                    if i > 0 and nums[i] == nums[i - 1] and not (mask & (1 << (i - 1))):
                        continue
                    nxt = cur_sum + nums[i]
                    if nxt > target:
                        continue
                    if dfs(mask | (1 << i), 0 if nxt == target else nxt):
                        return True

            failed[mask] = 1
            return False

        return dfs(0, 0)
