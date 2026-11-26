from itertools import permutations


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        res: List[List[str]] = []
        for perm in permutations(range(n)):
            if len({r - c for r, c in enumerate(perm)}) == n and len({r + c for r, c in enumerate(perm)}) == n:
                res.append(["." * c + "Q" + "." * (n - 1 - c) for c in perm])
        return res
