class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(arr)
        stack = []
        total = 0
        for i in range(n + 1):
            cur = arr[i] if i < n else 0
            while stack and arr[stack[-1]] >= cur:
                mid = stack.pop()
                left = stack[-1] if stack else -1
                total = (total + arr[mid] * (mid - left) * (i - mid)) % MOD
            stack.append(i)
        return total
