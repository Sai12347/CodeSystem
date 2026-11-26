class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        n, m = len(s), len(p)
        if m > n:
            return []
        target = Counter(p)
        res = []
        for i in range(n - m + 1):
            if Counter(s[i:i + m]) == target:
                res.append(i)
        return res
