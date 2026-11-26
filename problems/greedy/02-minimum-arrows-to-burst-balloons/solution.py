class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        points.sort(key=lambda p:p[1])
        arrows=0; end=None
        for left,right in points:
            if end is None or left>end:
                arrows+=1; end=right
        return arrows
