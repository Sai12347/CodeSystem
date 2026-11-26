class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        n = len(s)
        if n < 4 or n > 12:
            return []
        res: List[str] = []
        parts: List[str] = []

        def backtrack(start: int, seg: int) -> None:
            rem_chars = n - start
            rem_segs = 4 - seg
            if rem_chars < rem_segs or rem_chars > 3 * rem_segs:
                return
            if seg == 4:
                res.append(".".join(parts))
                return
            for length in range(1, min(3, rem_chars) + 1):
                if length > 1 and s[start] == "0":
                    break
                piece = s[start : start + length]
                if int(piece) <= 255:
                    parts.append(piece)
                    backtrack(start + length, seg + 1)
                    parts.pop()

        backtrack(0, 0)
        return res
