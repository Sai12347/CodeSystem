class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        n = len(s)
        res: List[str] = []

        def valid(p: str) -> bool:
            if not p or len(p) > 3:
                return False
            if len(p) > 1 and p[0] == "0":
                return False
            return int(p) <= 255

        for i in range(1, min(4, n)):
            for j in range(i + 1, min(i + 4, n)):
                for k in range(j + 1, min(j + 4, n)):
                    a, b, c, d = s[:i], s[i:j], s[j:k], s[k:]
                    if valid(a) and valid(b) and valid(c) and valid(d):
                        res.append(f"{a}.{b}.{c}.{d}")
        return res
