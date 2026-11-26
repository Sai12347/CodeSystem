class Solution:
    def smallestAllSetBits(self, n: int) -> int:
        return (1 << n.bit_length()) - 1
