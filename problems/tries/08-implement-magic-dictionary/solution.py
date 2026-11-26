class _Node:
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children = {}
        self.is_end = False


class MagicDictionary:
    def __init__(self) -> None:
        self.root = _Node()

    def buildDict(self, dictionary: List[str]) -> None:
        self.root = _Node()
        for word in dictionary:
            node = self.root
            for ch in word:
                nxt = node.children.get(ch)
                if nxt is None:
                    nxt = _Node()
                    node.children[ch] = nxt
                node = nxt
            node.is_end = True

    def search(self, searchWord: str) -> bool:
        n = len(searchWord)

        def dfs(idx: int, node: _Node, modified: bool) -> bool:
            if idx == n:
                return modified and node.is_end
            ch = searchWord[idx]
            nxt = node.children.get(ch)
            if nxt is not None and dfs(idx + 1, nxt, modified):
                return True
            if not modified:
                for c, child in node.children.items():
                    if c != ch and dfs(idx + 1, child, True):
                        return True
            return False

        return dfs(0, self.root, False)
