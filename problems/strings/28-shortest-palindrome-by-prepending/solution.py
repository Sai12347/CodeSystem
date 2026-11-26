class Solution:
    def shortestPalindrome(self, s: str) -> str:
        rev = s[::-1]
        seq = s + '#' + rev
        lps = [0] * len(seq)
        for i in range(1, len(seq)):
            j = lps[i - 1]
            while j and seq[i] != seq[j]: j = lps[j - 1]
            if seq[i] == seq[j]: j += 1
            lps[i] = j
        k = lps[-1]
        return rev[:len(s) - k] + s
