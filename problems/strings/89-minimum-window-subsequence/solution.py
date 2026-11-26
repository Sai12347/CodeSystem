class Solution:
    def minWindowSubsequence(self, s1: str, s2: str) -> str:
        n, m = len(s1), len(s2)
        best_start = -1
        best_len = n + 1
        i = 0
        while i < n:
            j = 0
            while i < n:
                if s1[i] == s2[j]:
                    j += 1
                    if j == m:
                        break
                i += 1
            if j < m:
                break
            end = i
            j = m - 1
            while j >= 0:
                if s1[i] == s2[j]:
                    j -= 1
                i -= 1
            start = i + 1
            if end - start + 1 < best_len:
                best_len = end - start + 1
                best_start = start
            i = start + 1
        return "" if best_start == -1 else s1[best_start:best_start + best_len]
