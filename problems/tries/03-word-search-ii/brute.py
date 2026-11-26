class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        rows, cols = len(board), len(board[0])

        def exists(word: str) -> bool:
            n = len(word)

            def dfs(r: int, c: int, i: int) -> bool:
                if board[r][c] != word[i]:
                    return False
                if i == n - 1:
                    return True
                saved = board[r][c]
                board[r][c] = "#"
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                        if dfs(nr, nc, i + 1):
                            board[r][c] = saved
                            return True
                board[r][c] = saved
                return False

            for r in range(rows):
                for c in range(cols):
                    if board[r][c] == word[0] and dfs(r, c, 0):
                        return True
            return False

        return [w for w in words if exists(w)]
