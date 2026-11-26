class Solution:
    def connectSticks(self, sticks: List[int]) -> int:
        arr = sorted(sticks)
        total = 0
        while len(arr) > 1:
            merged = arr.pop(0) + arr.pop(0)
            total += merged
            bisect.insort(arr, merged)
        return total
