class Solution:
    def solve(self, board: List[List[str]]) -> None:
        if not board or not board[0]:
            return
        rows, cols = len(board), len(board[0])
        q = deque()

        for r in range(rows):
            if board[r][0] == "O":
                board[r][0] = "S"
                q.append((r, 0))
            if board[r][cols - 1] == "O":
                board[r][cols - 1] = "S"
                q.append((r, cols - 1))
        for c in range(cols):
            if board[0][c] == "O":
                board[0][c] = "S"
                q.append((0, c))
            if board[rows - 1][c] == "O":
                board[rows - 1][c] = "S"
                q.append((rows - 1, c))

        while q:
            r, c = q.popleft()
            if r > 0 and board[r - 1][c] == "O":
                board[r - 1][c] = "S"
                q.append((r - 1, c))
            if r + 1 < rows and board[r + 1][c] == "O":
                board[r + 1][c] = "S"
                q.append((r + 1, c))
            if c > 0 and board[r][c - 1] == "O":
                board[r][c - 1] = "S"
                q.append((r, c - 1))
            if c + 1 < cols and board[r][c + 1] == "O":
                board[r][c + 1] = "S"
                q.append((r, c + 1))

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "S":
                    board[r][c] = "O"
