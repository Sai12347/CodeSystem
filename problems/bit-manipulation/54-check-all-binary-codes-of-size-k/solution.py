class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:
        need = 1 << k
        if len(s) - k + 1 < need:
            return False
        seen = bytearray(need)
        mask = need - 1
        code = 0
        for i, ch in enumerate(s):
            code = ((code << 1) & mask) | (ord(ch) - 48)
            if i >= k - 1 and not seen[code]:
                seen[code] = 1
                need -= 1
                if need == 0:
                    return True
        return False
