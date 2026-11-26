class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        m, n = len(s1), len(s2)
        if m > n:
            return False

        need = [0] * 26
        win = [0] * 26
        base = ord("a")

        for i in range(m):
            need[ord(s1[i]) - base] += 1
            win[ord(s2[i]) - base] += 1

        matches = sum(1 for c in range(26) if need[c] == win[c])
        if matches == 26:
            return True

        for right in range(m, n):
            add_idx = ord(s2[right]) - base
            if win[add_idx] == need[add_idx]:
                matches -= 1
            win[add_idx] += 1
            if win[add_idx] == need[add_idx]:
                matches += 1

            rem_idx = ord(s2[right - m]) - base
            if win[rem_idx] == need[rem_idx]:
                matches -= 1
            win[rem_idx] -= 1
            if win[rem_idx] == need[rem_idx]:
                matches += 1

            if matches == 26:
                return True

        return False
