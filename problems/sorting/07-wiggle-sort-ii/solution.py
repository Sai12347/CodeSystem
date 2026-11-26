import random


class Solution:
    def wiggleSort(self, nums: List[int]) -> None:
        n = len(nums)
        if n <= 1:
            return

        # Iterative 3-way Quickselect for median
        target = n // 2
        lo, hi = 0, n - 1
        rng = random.Random(42)
        median = nums[0]
        while lo <= hi:
            pivot = nums[rng.randint(lo, hi)]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if nums[i] < pivot:
                    nums[lt], nums[i] = nums[i], nums[lt]
                    lt += 1
                    i += 1
                elif nums[i] > pivot:
                    nums[i], nums[gt] = nums[gt], nums[i]
                    gt -= 1
                else:
                    i += 1
            if target < lt:
                hi = lt - 1
            elif target > gt:
                lo = gt + 1
            else:
                median = pivot
                break

        # Virtual index 3-way Dutch National Flag partition
        m = n | 1
        left, i, right = 0, 0, n - 1
        while i <= right:
            vi = (1 + 2 * i) % m
            if nums[vi] > median:
                vl = (1 + 2 * left) % m
                nums[vl], nums[vi] = nums[vi], nums[vl]
                left += 1
                i += 1
            elif nums[vi] < median:
                vr = (1 + 2 * right) % m
                nums[vi], nums[vr] = nums[vr], nums[vi]
                right -= 1
            else:
                i += 1
