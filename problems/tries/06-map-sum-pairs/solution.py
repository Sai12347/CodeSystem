class _Node:
    __slots__ = ("children", "score")

    def __init__(self) -> None:
        self.children = {}
        self.score = 0


class MapSum:
    def __init__(self) -> None:
        self.root = _Node()
        self.values = {}

    def insert(self, key: str, val: int) -> None:
        delta = val - self.values.get(key, 0)
        self.values[key] = val
        node = self.root
        for ch in key:
            nxt = node.children.get(ch)
            if nxt is None:
                nxt = _Node()
                node.children[ch] = nxt
            node = nxt
            node.score += delta

    def sum(self, prefix: str) -> int:
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return 0
        return node.score
