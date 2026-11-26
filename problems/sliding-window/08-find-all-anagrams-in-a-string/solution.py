class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        n, m = len(s), len(p)
        if m > n:
            return []
        need = [0] * 26
        win = [0] * 26
        base = ord("a")
        for ch in p:
            need[ord(ch) - base] += 1
        for i in range(m):
            win[ord(s[i]) - base] += 1

        matches = sum(1 for i in range(26) if need[i] == win[i])
        res = [0] if matches == 26 else []

        for right in range(m, n):
            add_idx = ord(s[right]) - base
            if win[add_idx] == need[add_idx]:
                matches -= 1
            win[add_idx] += 1
            if win[add_idx] == need[add_idx]:
                matches += 1

            rem_idx = ord(s[right - m]) - base
            if win[rem_idx] == need[rem_idx]:
                matches -= 1
            win[rem_idx] -= 1
            if win[rem_idx] == need[rem_idx]:
                matches += 1

            if matches == 26:
                res.append(right - m + 1)
        return res
