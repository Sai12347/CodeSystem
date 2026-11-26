class Solution:
    def intervalIntersection(self, firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:
        res = []
        for a, b in firstList:
            for c, d in secondList:
                lo = max(a, c)
                hi = min(b, d)
                if lo <= hi:
                    res.append([lo, hi])
        res.sort()
        return res
