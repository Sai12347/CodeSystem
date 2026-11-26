class Solution:
    def balancedString(self, s: str) -> int:
        n = len(s)
        target = n // 4
        cnt = {"Q": 0, "W": 0, "E": 0, "R": 0}
        for ch in s:
            cnt[ch] += 1

        if cnt["Q"] <= target and cnt["W"] <= target and cnt["E"] <= target and cnt["R"] <= target:
            return 0

        best = n
        left = 0
        for right, ch in enumerate(s):
            cnt[ch] -= 1
            while (
                left <= right
                and cnt["Q"] <= target
                and cnt["W"] <= target
                and cnt["E"] <= target
                and cnt["R"] <= target
            ):
                length = right - left + 1
                if length < best:
                    best = length
                cnt[s[left]] += 1
                left += 1

        return best
