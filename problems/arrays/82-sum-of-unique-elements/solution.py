class Solution:
    def sumOfUnique(self, nums: List[int]) -> int:
        counts = Counter(nums)
        return sum(x for x, count in counts.items() if count == 1)
