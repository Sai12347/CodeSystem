class _TrieNode:
    __slots__ = ("children", "word")

    def __init__(self) -> None:
        self.children = {}
        self.word = None


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = _TrieNode()
        for w in words:
            node = root
            for ch in w:
                nxt = node.children.get(ch)
                if nxt is None:
                    nxt = _TrieNode()
                    node.children[ch] = nxt
                node = nxt
            node.word = w

        rows, cols = len(board), len(board[0])
        found: List[str] = []

        def dfs(r: int, c: int, parent: _TrieNode) -> None:
            ch = board[r][c]
            node = parent.children.get(ch)
            if node is None:
                return
            if node.word is not None:
                found.append(node.word)
                node.word = None

            board[r][c] = "#"
            if r > 0 and board[r - 1][c] in node.children:
                dfs(r - 1, c, node)
            if r + 1 < rows and board[r + 1][c] in node.children:
                dfs(r + 1, c, node)
            if c > 0 and board[r][c - 1] in node.children:
                dfs(r, c - 1, node)
            if c + 1 < cols and board[r][c + 1] in node.children:
                dfs(r, c + 1, node)
            board[r][c] = ch

            if not node.children and node.word is None:
                del parent.children[ch]

        for r in range(rows):
            for c in range(cols):
                if board[r][c] in root.children:
                    dfs(r, c, root)
        return found
