class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i, v in enumerate(nums):
            prefix[i + 1] = prefix[i] + v
        dq = deque()
        best = n + 1
        for i, p in enumerate(prefix):
            while dq and p - prefix[dq[0]] >= k:
                length = i - dq.popleft()
                if length < best:
                    best = length
            while dq and prefix[dq[-1]] >= p:
                dq.pop()
            dq.append(i)
        return best if best <= n else -1
