class Solution:
    def countWalks(self, n: int, edges: List[List[int]], src: int, dst: int, k: int) -> int:
        MOD = 1_000_000_007
        base = [[0] * n for _ in range(n)]
        for u, v in edges:
            base[u][v] += 1
        res = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

        def mul(A, B):
            C = [[0] * n for _ in range(n)]
            for i in range(n):
                ai = A[i]
                ci = C[i]
                for mid in range(n):
                    v = ai[mid]
                    if v:
                        bm = B[mid]
                        for j in range(n):
                            ci[j] = (ci[j] + v * bm[j]) % MOD
            return C

        exp = k
        while exp > 0:
            if exp & 1:
                res = mul(res, base)
            base = mul(base, base)
            exp >>= 1
        return res[src][dst]
