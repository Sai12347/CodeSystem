class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        last_s = [0] * 256
        last_t = [0] * 256
        for i, (cs, ct) in enumerate(zip(s, t), 1):
            os_i, ot_i = ord(cs), ord(ct)
            if last_s[os_i] != last_t[ot_i]:
                return False
            last_s[os_i] = i
            last_t[ot_i] = i
        return True
