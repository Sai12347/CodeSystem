import re


class Solution:
    def myAtoi(self, s: str) -> int:
        m = re.match(r"^ *([+-]?)([0-9]+)", s)
        if not m:
            return 0
        val = int(m.group(1) + m.group(2))
        return max(-2147483648, min(2147483647, val))
