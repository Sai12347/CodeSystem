class Solution:
    def countKDifference(self, nums: List[int], k: int) -> int:
        counts = Counter(nums)
        if k == 0: return sum(c * (c - 1) // 2 for c in counts.values())
        return sum(c * counts.get(x + k, 0) for x, c in counts.items())
