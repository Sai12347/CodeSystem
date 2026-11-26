class Solution:
    def zOrderTraversal(self, grid: List[List[int]]) -> List[int]:
        n = len(grid)
        res = []

        def dfs(r: int, c: int, size: int) -> None:
            if size == 1:
                res.append(grid[r][c])
                return
            h = size // 2
            dfs(r, c, h)
            dfs(r, c + h, h)
            dfs(r + h, c, h)
            dfs(r + h, c + h, h)

        dfs(0, 0, n)
        return res
