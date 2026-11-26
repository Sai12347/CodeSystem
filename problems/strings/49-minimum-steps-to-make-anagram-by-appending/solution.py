class Solution:
    def minStepsToAnagram(self, s: str, t: str) -> int:
        diff = [0] * 26
        for ch in s:
            diff[ord(ch) - 97] += 1
        for ch in t:
            diff[ord(ch) - 97] -= 1
        return sum(abs(v) for v in diff)
