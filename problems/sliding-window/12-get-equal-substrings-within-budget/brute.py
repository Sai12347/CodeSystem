class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        n = len(s)
        costs = [abs(ord(s[i]) - ord(t[i])) for i in range(n)]
        best = 0
        for i in range(n):
            total = 0
            for j in range(i, n):
                total += costs[j]
                if total > maxCost:
                    break
                if j - i + 1 > best:
                    best = j - i + 1
        return best
