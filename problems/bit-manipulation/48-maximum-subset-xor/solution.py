class Solution:
    def maxSubsetXor(self, nums: List[int]) -> int:
        basis = [0] * 31
        for x in nums:
            for b in range(30, -1, -1):
                if (x >> b) & 1:
                    if basis[b] == 0:
                        basis[b] = x
                        break
                    x ^= basis[b]
        ans = 0
        for b in range(30, -1, -1):
            if (ans ^ basis[b]) > ans:
                ans ^= basis[b]
        return ans
