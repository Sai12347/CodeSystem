class Solution:
    def isValid(self, s: str) -> bool:
        # Independent reduction brute force: repeatedly delete all "abc" substrings.
        while "abc" in s:
            s = s.replace("abc", "")
        return s == ""
