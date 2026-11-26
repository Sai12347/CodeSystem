class Solution:
    def findAllConcatenatedWordsInADict(self, words: List[str]) -> List[str]:
        word_set = set(words)
        res = []
        for w in words:
            n = len(w)
            dp = [False] * (n + 1)
            dp[0] = True
            for i in range(1, n + 1):
                for j in range(0 if i < n else 1, i):
                    if dp[j] and w[j:i] in word_set:
                        dp[i] = True
                        break
            if dp[n]:
                res.append(w)
        return res
