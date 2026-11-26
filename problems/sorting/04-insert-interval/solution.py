class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        res = []
        ns, ne = newInterval
        i, n = 0, len(intervals)
        while i < n and intervals[i][1] < ns:
            res.append(intervals[i])
            i += 1
        while i < n and intervals[i][0] <= ne:
            if intervals[i][0] < ns:
                ns = intervals[i][0]
            if intervals[i][1] > ne:
                ne = intervals[i][1]
            i += 1
        res.append([ns, ne])
        while i < n:
            res.append(intervals[i])
            i += 1
        return res
