class Solution:
    def minSteps(self, s: str, t: str) -> int:
        diff = [0] * 26
        for a, b in zip(s, t):
            diff[ord(a) - 97] += 1
            diff[ord(b) - 97] -= 1
        return sum(v for v in diff if v > 0)
