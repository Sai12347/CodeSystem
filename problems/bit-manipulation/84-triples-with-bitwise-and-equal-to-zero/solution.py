class Solution:
    def countTriplets(self, nums: List[int]) -> int:
        max_val = max(nums)
        n = len(nums)
        if max_val == 0:
            return n * n * n
        bits = max_val.bit_length()
        size = 1 << bits
        full = size - 1
        freq = {}
        for x in nums:
            freq[x] = freq.get(x, 0) + 1
        items = list(freq.items())
        dp = [0] * size
        m = len(items)
        for i in range(m):
            a, ca = items[i]
            dp[a] += ca * ca
            for j in range(i + 1, m):
                b, cb = items[j]
                dp[a & b] += 2 * ca * cb
        for b in range(bits):
            bit = 1 << b
            step = bit << 1
            for start in range(bit, size, step):
                for mask in range(start, start + bit):
                    dp[mask] += dp[mask ^ bit]
        ans = 0
        for x, cx in items:
            ans += cx * dp[full ^ x]
        return ans
