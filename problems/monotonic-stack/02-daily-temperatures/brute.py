class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        ans = [0] * n
        for i in range(n):
            ti = temperatures[i]
            for j in range(i + 1, n):
                if temperatures[j] > ti:
                    ans[i] = j - i
                    break
        return ans
