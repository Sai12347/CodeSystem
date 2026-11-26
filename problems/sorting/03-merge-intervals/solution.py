class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda iv: (iv[0], iv[1]))
        merged = [list(intervals[0])]
        for s, e in intervals[1:]:
            if s <= merged[-1][1]:
                if e > merged[-1][1]:
                    merged[-1][1] = e
            else:
                merged.append([s, e])
        return merged
