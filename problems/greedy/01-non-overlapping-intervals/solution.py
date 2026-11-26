class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x:x[1]);end=float('-inf');kept=0
        for a,b in intervals:
            if a>=end:kept+=1;end=b
        return len(intervals)-kept
