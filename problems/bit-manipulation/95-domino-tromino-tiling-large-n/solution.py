class Solution:
    def numTilingsLargeN(self, n: int) -> int:
        MOD = 1_000_000_007
        if n == 1:
            return 1
        if n == 2:
            return 2

        def mul(A, B):
            C = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            for i in range(3):
                for k in range(3):
                    v = A[i][k]
                    if v:
                        for j in range(3):
                            C[i][j] = (C[i][j] + v * B[k][j]) % MOD
            return C

        res = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        base = [[2, 0, 1], [1, 0, 0], [0, 1, 0]]
        exp = n - 2
        while exp > 0:
            if exp & 1:
                res = mul(res, base)
            base = mul(base, base)
            exp >>= 1
        return (res[0][0] * 2 + res[0][1] + res[0][2]) % MOD
