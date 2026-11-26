class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        rows = [0] * 9
        cols = [0] * 9
        boxes = [0] * 9
        empties: List[tuple[int, int]] = []

        for r in range(9):
            for c in range(9):
                ch = board[r][c]
                if ch == ".":
                    empties.append((r, c))
                else:
                    bit = 1 << (ord(ch) - ord("1"))
                    rows[r] |= bit
                    cols[c] |= bit
                    boxes[(r // 3) * 3 + (c // 3)] |= bit

        n = len(empties)

        def dfs(idx: int) -> bool:
            if idx == n:
                return True
            best = idx
            best_cnt = 10
            best_mask = 0
            for i in range(idx, n):
                r, c = empties[i]
                bi = (r // 3) * 3 + (c // 3)
                avail = 0x1FF & ~(rows[r] | cols[c] | boxes[bi])
                cnt = avail.bit_count()
                if cnt == 0:
                    return False
                if cnt < best_cnt:
                    best_cnt = cnt
                    best = i
                    best_mask = avail
                    if cnt == 1:
                        break

            empties[idx], empties[best] = empties[best], empties[idx]
            r, c = empties[idx]
            bi = (r // 3) * 3 + (c // 3)
            m = best_mask
            while m:
                bit = m & -m
                m ^= bit
                digit = bit.bit_length()
                board[r][c] = chr(ord("0") + digit)
                rows[r] |= bit
                cols[c] |= bit
                boxes[bi] |= bit
                if dfs(idx + 1):
                    return True
                rows[r] ^= bit
                cols[c] ^= bit
                boxes[bi] ^= bit
                board[r][c] = "."
            empties[idx], empties[best] = empties[best], empties[idx]
            return False

        dfs(0)
