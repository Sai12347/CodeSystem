class Solution:
    def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
        dq = deque()
        best = nums[0]
        for i, val in enumerate(nums):
            while dq and dq[0][0] < i - k:
                dq.popleft()
            cur = val + (dq[0][1] if dq and dq[0][1] > 0 else 0)
            if cur > best:
                best = cur
            while dq and dq[-1][1] <= cur:
                dq.pop()
            dq.append((i, cur))
        return best
