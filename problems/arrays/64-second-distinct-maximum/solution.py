class Solution:
    def secondDistinctMaximum(self, nums: List[int]) -> int:
        first = second = None
        for x in nums:
            if x == first or x == second: continue
            if first is None or x > first: second, first = first, x
            elif second is None or x > second: second = x
        return -1 if second is None else second
