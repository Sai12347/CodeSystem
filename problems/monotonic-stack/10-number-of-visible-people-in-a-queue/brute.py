class Solution:
    def canSeePersonsCount(self, heights: List[int]) -> List[int]:
        n = len(heights)
        ans = [0] * n
        for i in range(n):
            hi = heights[i]
            max_between = 0
            cnt = 0
            for j in range(i + 1, n):
                hj = heights[j]
                if hj > max_between:
                    cnt += 1
                    max_between = hj
                if hj > hi:
                    break
            ans[i] = cnt
        return ans
