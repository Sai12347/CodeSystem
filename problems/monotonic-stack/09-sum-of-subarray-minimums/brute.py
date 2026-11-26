class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(arr)
        total = 0
        for i in range(n):
            mn = arr[i]
            for j in range(i, n):
                if arr[j] < mn:
                    mn = arr[j]
                total += mn
            total %= MOD
        return total
