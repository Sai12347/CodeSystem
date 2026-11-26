class _Node:
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children = {}
        self.is_end = False


class WordDictionary:
    def __init__(self) -> None:
        self.root = _Node()

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            nxt = node.children.get(ch)
            if nxt is None:
                nxt = _Node()
                node.children[ch] = nxt
            node = nxt
        node.is_end = True

    def search(self, word: str) -> bool:
        n = len(word)

        def dfs(idx: int, node: _Node) -> bool:
            if idx == n:
                return node.is_end
            ch = word[idx]
            if ch == ".":
                for child in node.children.values():
                    if dfs(idx + 1, child):
                        return True
                return False
            nxt = node.children.get(ch)
            return nxt is not None and dfs(idx + 1, nxt)

        return dfs(0, self.root)
