class Solution:
    def postfixPeakDepth(self, tokens: List[str]) -> int:
        h = 0
        peak = 0
        for tok in tokens:
            if tok == "neg" or tok == "abs":
                if h < 1:
                    return -1
            elif tok in ("+", "-", "*", "/"):
                if h < 2:
                    return -1
                h -= 1
            else:
                h += 1
                if h > peak:
                    peak = h
        return peak if h == 1 else -1
