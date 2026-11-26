class Solution:
    def updateBoard(self, board: List[List[str]], click: List[int]) -> List[List[str]]:
        from collections import deque
        m, n = len(board), len(board[0])
        res = [row[:] for row in board]
        sr, sc = click[0], click[1]
        if res[sr][sc] == 'M':
            res[sr][sc] = 'X'
            return res
        q = deque([(sr, sc)])
        visited = [[False] * n for _ in range(m)]
        visited[sr][sc] = True
        while q:
            r, c = q.popleft()
            mines = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and res[nr][nc] == 'M':
                        mines += 1
            if mines > 0:
                res[r][c] = str(mines)
            else:
                res[r][c] = 'B'
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc] and res[nr][nc] == 'E':
                            visited[nr][nc] = True
                            q.append((nr, nc))
        return res
