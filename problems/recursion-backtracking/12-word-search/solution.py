class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])
        L = len(word)
        if L > m * n:
            return False

        board_cnt = Counter(ch for row in board for ch in row)
        word_cnt = Counter(word)
        for ch, need in word_cnt.items():
            if board_cnt[ch] < need:
                return False

        if board_cnt[word[0]] > board_cnt[word[-1]]:
            word = word[::-1]

        def dfs(r: int, c: int, idx: int) -> bool:
            if board[r][c] != word[idx]:
                return False
            if idx == L - 1:
                return True
            saved = board[r][c]
            board[r][c] = "#"
            nxt = idx + 1
            if r > 0 and dfs(r - 1, c, nxt):
                board[r][c] = saved
                return True
            if r + 1 < m and dfs(r + 1, c, nxt):
                board[r][c] = saved
                return True
            if c > 0 and dfs(r, c - 1, nxt):
                board[r][c] = saved
                return True
            if c + 1 < n and dfs(r, c + 1, nxt):
                board[r][c] = saved
                return True
            board[r][c] = saved
            return False

        for r in range(m):
            for c in range(n):
                if board[r][c] == word[0] and dfs(r, c, 0):
                    return True
        return False
