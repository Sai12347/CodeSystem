class Solution:
    def partitionString(self, s: str) -> int:
        parts = 1
        mask = 0
        for ch in s:
            bit = 1 << (ord(ch) - 97)
            if mask & bit:
                parts += 1
                mask = bit
            else:
                mask |= bit
        return parts
