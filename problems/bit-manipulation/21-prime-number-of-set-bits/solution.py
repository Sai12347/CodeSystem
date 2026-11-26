class Solution:
    def countPrimeSetBits(self, left: int, right: int) -> int:
        prime_mask = 665772
        ans = 0
        for x in range(left, right + 1):
            if (prime_mask >> x.bit_count()) & 1:
                ans += 1
        return ans
