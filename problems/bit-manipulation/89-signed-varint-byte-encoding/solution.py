class Solution:
    def encodeSignedVarint(self, n: int) -> List[int]:
        u = ((n << 1) ^ (n >> 31)) & 0xFFFFFFFF
        out = []
        while u >= 0x80:
            out.append((u & 0x7F) | 0x80)
            u >>= 7
        out.append(u)
        return out
