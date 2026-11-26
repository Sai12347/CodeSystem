class Solution:
    def canSeePersonsCount(self, heights: List[int]) -> List[int]:
        n = len(heights)
        ans = [0] * n
        stack = []
        for i in range(n - 1, -1, -1):
            h = heights[i]
            visible = 0
            while stack and stack[-1] < h:
                stack.pop()
                visible += 1
            if stack:
                visible += 1
            ans[i] = visible
            stack.append(h)
        return ans
