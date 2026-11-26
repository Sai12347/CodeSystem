class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0
        arr = sorted(set(nums))
        best = 1
        run = 1
        for i in range(1, len(arr)):
            if arr[i] == arr[i - 1] + 1:
                run += 1
                if run > best:
                    best = run
            else:
                run = 1
        return best
