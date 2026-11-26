class Solution:
    def findLongestWord(self, s: str, dictionary: List[str]) -> str:
        best = ""
        n = len(s)
        for w in dictionary:
            if len(w) < len(best) or (len(w) == len(best) and w >= best):
                continue
            i = j = 0
            m = len(w)
            while i < n and j < m:
                if s[i] == w[j]:
                    j += 1
                i += 1
            if j == m:
                best = w
        return best
