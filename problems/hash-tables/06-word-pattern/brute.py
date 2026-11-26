class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split(" ")
        if len(words) != len(pattern):
            return False
        p_idx = [pattern.index(c) for c in pattern]
        w_idx = [words.index(w) for w in words]
        return p_idx == w_idx
