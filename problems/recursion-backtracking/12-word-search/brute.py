class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])

        def dfs(r: int, c: int, i: int, vis: set) -> bool:
            if board[r][c] != word[i]:
                return False
            if i == len(word) - 1:
                return True
            vis.add((r, c))
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in vis:
                    if dfs(nr, nc, i + 1, vis):
                        vis.remove((r, c))
                        return True
            vis.remove((r, c))
            return False

        for r in range(m):
            for c in range(n):
                if dfs(r, c, 0, set()):
                    return True
        return False
