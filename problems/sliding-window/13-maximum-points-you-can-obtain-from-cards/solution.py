class Solution:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        n = len(cardPoints)
        cur = sum(cardPoints[:k])
        best = cur
        for i in range(1, k + 1):
            cur += cardPoints[n - i] - cardPoints[k - i]
            if cur > best:
                best = cur
        return best
