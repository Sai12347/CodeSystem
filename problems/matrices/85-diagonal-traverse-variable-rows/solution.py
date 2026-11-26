class Solution:
    def findDiagonalOrder(self, nums: List[List[int]]) -> List[int]:
        buckets = []
        total = 0
        for r in range(len(nums) - 1, -1, -1):
            row = nums[r]
            total += len(row)
            for c, val in enumerate(row):
                d = r + c
                while len(buckets) <= d:
                    buckets.append([])
                buckets[d].append(val)
        res = []
        for b in buckets:
            res.extend(b)
        return res
