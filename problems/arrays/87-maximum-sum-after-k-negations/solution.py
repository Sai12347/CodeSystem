class Solution:
    def largestSumAfterKNegations(self, nums: List[int], k: int) -> int:
        a = sorted(nums)
        for i in range(len(a)):
            if k and a[i] < 0: a[i] = -a[i]; k -= 1
        total = sum(a)
        if k % 2: total -= 2 * min(a)
        return total
