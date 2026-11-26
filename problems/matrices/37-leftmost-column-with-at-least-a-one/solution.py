class Solution:
    def leftmostColumnWithOne(self, mat: List[List[int]]) -> int:
        m, n = len(mat), len(mat[0])
        r, c = 0, n - 1
        ans = -1
        while r < m and c >= 0:
            if mat[r][c] == 1:
                ans = c
                c -= 1
            else:
                r += 1
        return ans
