class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        seen = set()
        for mask in range(1 << n):
            sub = tuple(sorted(nums[i] for i in range(n) if (mask >> i) & 1))
            seen.add(sub)
        return [list(t) for t in sorted(seen)]
