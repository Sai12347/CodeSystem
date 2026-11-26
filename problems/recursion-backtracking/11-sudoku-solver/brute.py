class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        empties = []
        for r in range(9):
            for c in range(9):
                ch = board[r][c]
                if ch == ".":
                    empties.append((r, c))
                else:
                    rows[r].add(ch)
                    cols[c].add(ch)
                    boxes[(r // 3) * 3 + (c // 3)].add(ch)

        digits = "123456789"

        def backtrack(idx: int) -> bool:
            if idx == len(empties):
                return True
            r, c = empties[idx]
            bi = (r // 3) * 3 + (c // 3)
            for d in digits:
                if d not in rows[r] and d not in cols[c] and d not in boxes[bi]:
                    board[r][c] = d
                    rows[r].add(d)
                    cols[c].add(d)
                    boxes[bi].add(d)
                    if backtrack(idx + 1):
                        return True
                    board[r][c] = "."
                    rows[r].remove(d)
                    cols[c].remove(d)
                    boxes[bi].remove(d)
            return False

        backtrack(0)
