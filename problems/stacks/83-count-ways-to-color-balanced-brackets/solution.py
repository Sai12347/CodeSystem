class Solution:
    def countBracketColorings(self, s: str) -> int:
        MOD = 10**9 + 7
        VALID_PAIRS = ((0, 1), (0, 2), (1, 0), (2, 0))

        def merge(a, b):
            if a is None:
                return b
            res = [[0] * 3 for _ in range(3)]
            for l1 in range(3):
                for r1 in range(3):
                    va = a[l1][r1]
                    if va == 0:
                        continue
                    for l2 in range(3):
                        if r1 != 0 and r1 == l2:
                            continue
                        for r2 in range(3):
                            vb = b[l2][r2]
                            if vb:
                                res[l1][r2] = (res[l1][r2] + va * vb) % MOD
            return res

        frames = [None]
        for ch in s:
            if ch == '(':
                frames.append(None)
            else:
                inner = frames.pop()
                block = [[0] * 3 for _ in range(3)]
                if inner is None:
                    for cl, cr in VALID_PAIRS:
                        block[cl][cr] = 1
                else:
                    for cl, cr in VALID_PAIRS:
                        tot = 0
                        for a in range(3):
                            if cl != 0 and cl == a:
                                continue
                            for b in range(3):
                                if cr != 0 and cr == b:
                                    continue
                                tot += inner[a][b]
                        block[cl][cr] = tot % MOD
                frames[-1] = merge(frames[-1], block)

        root = frames[0]
        ans = 0
        for r in root:
            for v in r:
                ans = (ans + v) % MOD
        return ans
