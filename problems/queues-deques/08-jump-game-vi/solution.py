class Solution:
    def maxResult(self, nums: List[int], k: int) -> int:
        dq = deque([(0, nums[0])])
        for i in range(1, len(nums)):
            while dq[0][0] < i - k:
                dq.popleft()
            cur = nums[i] + dq[0][1]
            while dq and dq[-1][1] <= cur:
                dq.pop()
            dq.append((i, cur))
        return dq[-1][1]
