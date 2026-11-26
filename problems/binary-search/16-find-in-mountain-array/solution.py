# This is MountainArray's API interface.
# class MountainArray:
#     def get(self, index: int) -> int:
#     def length(self) -> int:

class Solution:
    def findInMountainArray(self, target: int, mountainArr: 'MountainArray') -> int:
        n = mountainArr.length()

        # 1. Find the peak index in [1, n - 2]
        lo, hi = 1, n - 2
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if mountainArr.get(mid) < mountainArr.get(mid + 1):
                lo = mid + 1
            else:
                hi = mid
        peak = lo

        # 2. Binary search strictly increasing left half [0, peak]
        lo, hi = 0, peak
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            val = mountainArr.get(mid)
            if val == target:
                return mid
            if val < target:
                lo = mid + 1
            else:
                hi = mid - 1

        # 3. Binary search strictly decreasing right half [peak + 1, n - 1]
        lo, hi = peak + 1, n - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            val = mountainArr.get(mid)
            if val == target:
                return mid
            if val > target:
                lo = mid + 1
            else:
                hi = mid - 1

        return -1
