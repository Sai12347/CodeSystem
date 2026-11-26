class Solution:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        n = len(cardPoints)
        best = 0
        for left in range(k + 1):
            right = k - left
            score = sum(cardPoints[:left]) + (sum(cardPoints[n - right :]) if right else 0)
            if score > best:
                best = score
        return best
