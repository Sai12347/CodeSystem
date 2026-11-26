class Solution:
    def movesToChessboard(self, board: List[List[int]]) -> int:
        n = len(board)
        for r in range(n):
            for c in range(n):
                if (board[0][0] ^ board[r][0] ^ board[0][c] ^ board[r][c]) != 0:
                    return -1

        row_sum = col_sum = row_swap = col_swap = 0
        for i in range(n):
            row_sum += board[0][i]
            col_sum += board[i][0]
            if board[i][0] == i % 2:
                row_swap += 1
            if board[0][i] == i % 2:
                col_swap += 1

        if row_sum != n // 2 and row_sum != (n + 1) // 2:
            return -1
        if col_sum != n // 2 and col_sum != (n + 1) // 2:
            return -1

        if n % 2 == 1:
            if row_swap % 2 == 1:
                row_swap = n - row_swap
            if col_swap % 2 == 1:
                col_swap = n - col_swap
        else:
            row_swap = min(row_swap, n - row_swap)
            col_swap = min(col_swap, n - col_swap)
        return (row_swap + col_swap) // 2
