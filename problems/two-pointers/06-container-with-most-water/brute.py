class Solution:
    def maxArea(self, height: List[int]) -> int:
        n = len(height)
        best = 0
        for i in range(n):
            hi = height[i]
            if hi * (n - 1 - i) <= best:
                continue
            for j in range(i + 1, n):
                hj = height[j]
                area = (hi if hi < hj else hj) * (j - i)
                if area > best:
                    best = area
        return best
