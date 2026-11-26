class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        n = len(profits)
        used = [False] * n
        for _ in range(min(k, n)):
            best = -1
            for i in range(n):
                if not used[i] and capital[i] <= w:
                    if best == -1 or profits[i] > profits[best]:
                        best = i
            if best == -1:
                break
            used[best] = True
            w += profits[best]
        return w
