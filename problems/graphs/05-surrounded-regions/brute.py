class Solution:
    def solve(self, board: List[List[str]]) -> None:
        if not board or not board[0]:
            return
        rows, cols = len(board), len(board[0])
        visited = [[False] * cols for _ in range(rows)]

        for r in range(rows):
            for c in range(cols):
                if board[r][c] != "O" or visited[r][c]:
                    continue
                comp = []
                touches_border = False
                q = deque([(r, c)])
                visited[r][c] = True
                while q:
                    cr, cc = q.popleft()
                    comp.append((cr, cc))
                    if cr == 0 or cr == rows - 1 or cc == 0 or cc == cols - 1:
                        touches_border = True
                    for nr, nc in ((cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)):
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and board[nr][nc] == "O":
                            visited[nr][nc] = True
                            q.append((nr, nc))
                if not touches_border:
                    for cr, cc in comp:
                        board[cr][cc] = "X"
