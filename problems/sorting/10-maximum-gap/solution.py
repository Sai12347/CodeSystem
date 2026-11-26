class Solution:
    def maximumGap(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 2:
            return 0
        mn = min(nums)
        mx = max(nums)
        if mn == mx:
            return 0
        bucket_size = max(1, (mx - mn) // (n - 1))
        bucket_count = (mx - mn) // bucket_size + 1
        b_min = [None] * bucket_count
        b_max = [None] * bucket_count
        for x in nums:
            idx = (x - mn) // bucket_size
            if b_min[idx] is None:
                b_min[idx] = b_max[idx] = x
            else:
                if x < b_min[idx]:
                    b_min[idx] = x
                if x > b_max[idx]:
                    b_max[idx] = x
        max_gap = 0
        prev_max = mn
        for i in range(bucket_count):
            if b_min[i] is None:
                continue
            gap = b_min[i] - prev_max
            if gap > max_gap:
                max_gap = gap
            prev_max = b_max[i]
        return max_gap
