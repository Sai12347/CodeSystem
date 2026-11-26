class Solution:
    def customSortString(self, order: str, s: str) -> str:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - 97] += 1
        out = []
        for ch in order:
            idx = ord(ch) - 97
            if counts[idx]:
                out.append(ch * counts[idx])
                counts[idx] = 0
        for idx in range(26):
            if counts[idx]:
                out.append(chr(97 + idx) * counts[idx])
        return "".join(out)
