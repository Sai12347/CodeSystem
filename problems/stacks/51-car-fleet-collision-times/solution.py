class Solution:
    def getCollisionTimes(self, cars: List[List[int]]) -> List[float]:
        n = len(cars)
        ans = [-1.0] * n
        stack = []
        for i in range(n - 1, -1, -1):
            p, s = cars[i]
            while stack:
                j = stack[-1]
                pj, sj = cars[j]
                if s <= sj or (ans[j] > 0 and (pj - p) / (s - sj) >= ans[j]):
                    stack.pop()
                else:
                    break
            if stack:
                j = stack[-1]
                ans[i] = (cars[j][0] - p) / (s - cars[j][1])
            stack.append(i)
        return ans
