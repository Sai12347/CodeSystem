class Solution:
    def buddyStrings(self, s: str, goal: str) -> bool:
        if len(s) != len(goal): return False
        diff = [i for i in range(len(s)) if s[i] != goal[i]]
        if not diff:
            return len(set(s)) < len(s)
        return len(diff) == 2 and s[diff[0]] == goal[diff[1]] and s[diff[1]] == goal[diff[0]]
