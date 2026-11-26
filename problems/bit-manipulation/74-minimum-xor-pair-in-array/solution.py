class Solution:
    def minXorPair(self, nums: List[int]) -> int:
        arr = sorted(nums)
        ans = arr[0] ^ arr[1]
        for i in range(1, len(arr) - 1):
            v = arr[i] ^ arr[i + 1]
            if v < ans:
                ans = v
        return ans
