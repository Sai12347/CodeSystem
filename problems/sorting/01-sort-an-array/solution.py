class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        if n <= 1:
            return nums
        buf = [0] * n

        def merge_sort(lo: int, hi: int) -> None:
            if hi - lo <= 1:
                return
            mid = (lo + hi) // 2
            merge_sort(lo, mid)
            merge_sort(mid, hi)
            if nums[mid - 1] <= nums[mid]:
                return
            i, j, k = lo, mid, lo
            while i < mid and j < hi:
                if nums[i] <= nums[j]:
                    buf[k] = nums[i]
                    i += 1
                else:
                    buf[k] = nums[j]
                    j += 1
                k += 1
            while i < mid:
                buf[k] = nums[i]
                i += 1
                k += 1
            while j < hi:
                buf[k] = nums[j]
                j += 1
                k += 1
            nums[lo:hi] = buf[lo:hi]

        merge_sort(0, n)
        return nums
