class Solution:
    def maxBallPassingScore(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        up = list(receiver)
        w = list(receiver)
        pos = list(range(n))
        score = list(range(n))
        rem = k
        while rem > 0:
            if rem & 1:
                for i in range(n):
                    p = pos[i]
                    score[i] += w[p]
                    pos[i] = up[p]
            rem >>= 1
            if rem > 0:
                new_up = [0] * n
                new_w = [0] * n
                for i in range(n):
                    mid = up[i]
                    new_up[i] = up[mid]
                    new_w[i] = w[i] + w[mid]
                up = new_up
                w = new_w
        return max(score)
