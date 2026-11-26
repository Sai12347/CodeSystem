class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        all_iv = sorted([list(x) for x in intervals] + [list(newInterval)])
        merged = [all_iv[0]]
        for s, e in all_iv[1:]:
            if s <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], e)
            else:
                merged.append([s, e])
        return merged
