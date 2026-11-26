class Solution:
    def countVowelPermutation(self, n: int) -> int:
        MOD = 1_000_000_007

        def mul(A, B):
            C = [[0] * 5 for _ in range(5)]
            for i in range(5):
                ai = A[i]
                ci = C[i]
                for k in range(5):
                    v = ai[k]
                    if v:
                        bk = B[k]
                        for j in range(5):
                            ci[j] = (ci[j] + v * bk[j]) % MOD
            return C

        res = [[1 if i == j else 0 for j in range(5)] for i in range(5)]
        base = [
            [0, 1, 1, 0, 1],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0],
        ]
        exp = n - 1
        while exp > 0:
            if exp & 1:
                res = mul(res, base)
            base = mul(base, base)
            exp >>= 1
        return sum(sum(row) for row in res) % MOD
