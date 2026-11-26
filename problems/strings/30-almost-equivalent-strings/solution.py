class Solution:
    def checkAlmostEquivalent(self, word1: str, word2: str) -> bool:
        counts = [0] * 26
        for c in word1: counts[ord(c) - 97] += 1
        for c in word2: counts[ord(c) - 97] -= 1
        return all(abs(x) <= 3 for x in counts)
