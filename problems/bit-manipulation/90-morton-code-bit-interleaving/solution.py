class Solution:
    def mortonEncode(self, x: int, y: int) -> int:
        def spread(v: int) -> int:
            v = (v | (v << 8)) & 0x00FF00FF
            v = (v | (v << 4)) & 0x0F0F0F0F
            v = (v | (v << 2)) & 0x33333333
            v = (v | (v << 1)) & 0x55555555
            return v

        return spread(x) | (spread(y) << 1)
