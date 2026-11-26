class Solution:
    def hIndex(self, citations: List[int]) -> int:
        # Independent sort-descending check
        s = sorted(citations, reverse=True)
        h = 0
        for i, c in enumerate(s):
            if c >= i + 1:
                h = i + 1
            else:
                break
        return h
