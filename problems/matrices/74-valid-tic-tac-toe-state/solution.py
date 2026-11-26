class Solution:
    def validTicTacToe(self, board: List[str]) -> bool:
        x_cnt = sum(row.count('X') for row in board)
        o_cnt = sum(row.count('O') for row in board)
        if x_cnt != o_cnt and x_cnt != o_cnt + 1:
            return False

        def wins(ch: str) -> bool:
            for i in range(3):
                if board[i][0] == board[i][1] == board[i][2] == ch:
                    return True
                if board[0][i] == board[1][i] == board[2][i] == ch:
                    return True
            if board[0][0] == board[1][1] == board[2][2] == ch:
                return True
            if board[0][2] == board[1][1] == board[2][0] == ch:
                return True
            return False

        x_win = wins('X')
        o_win = wins('O')
        if x_win and o_win:
            return False
        if x_win and x_cnt != o_cnt + 1:
            return False
        if o_win and x_cnt != o_cnt:
            return False
        return True
