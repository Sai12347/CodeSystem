class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        m, n = len(board), len(board[0])
        for r in range(m):
            for c in range(n):
                live = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n and (board[nr][nc] & 1):
                            live += 1
                if (board[r][c] & 1) == 1:
                    if live == 2 or live == 3:
                        board[r][c] |= 2
                elif live == 3:
                    board[r][c] |= 2
        for r in range(m):
            for c in range(n):
                board[r][c] >>= 1
