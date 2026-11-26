class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        def ok(vals):
            digits = [v for v in vals if v != "."]
            return len(digits) == len(set(digits))

        for r in range(9):
            if not ok(board[r]):
                return False
        for c in range(9):
            if not ok(board[r][c] for r in range(9)):
                return False
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                if not ok(board[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)):
                    return False
        return True
