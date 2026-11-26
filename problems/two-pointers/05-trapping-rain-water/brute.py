class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n < 3:
            return 0
        pref = [0] * n
        suff = [0] * n
        pref[0] = height[0]
        for i in range(1, n):
            pref[i] = max(pref[i - 1], height[i])
        suff[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            suff[i] = max(suff[i + 1], height[i])
        return sum(min(pref[i], suff[i]) - height[i] for i in range(n))
