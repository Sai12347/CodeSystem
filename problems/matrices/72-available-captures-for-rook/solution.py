class Solution:
    def numRookCaptures(self, board: List[List[str]]) -> int:
        m, n = len(board), len(board[0])
        rr = rc = 0
        for r in range(m):
            for c in range(n):
                if board[r][c] == 'R':
                    rr, rc = r, c
                    break
        captures = 0
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r, c = rr + dr, rc + dc
            while 0 <= r < m and 0 <= c < n:
                ch = board[r][c]
                if ch == 'B':
                    break
                if ch == 'p':
                    captures += 1
                    break
                r += dr
                c += dc
        return captures
