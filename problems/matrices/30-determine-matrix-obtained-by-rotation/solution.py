class Solution:
    def findRotation(self, mat: List[List[int]], target: List[List[int]]) -> bool:
        n = len(mat)
        ok0 = ok90 = ok180 = ok270 = True
        for r in range(n):
            for c in range(n):
                v = mat[r][c]
                if v != target[r][c]:
                    ok0 = False
                if v != target[c][n - 1 - r]:
                    ok90 = False
                if v != target[n - 1 - r][n - 1 - c]:
                    ok180 = False
                if v != target[n - 1 - c][r]:
                    ok270 = False
        return ok0 or ok90 or ok180 or ok270
