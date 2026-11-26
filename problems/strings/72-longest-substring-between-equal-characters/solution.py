class Solution:
    def maxLengthBetweenEqualCharacters(self, s: str) -> int:
        first = [-1] * 26
        best = -1
        for i, ch in enumerate(s):
            idx = ord(ch) - 97
            if first[idx] == -1:
                first[idx] = i
            else:
                best = max(best, i - first[idx] - 1)
        return best
