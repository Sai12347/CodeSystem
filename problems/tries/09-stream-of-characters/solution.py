class _Node:
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children = {}
        self.is_end = False


class StreamChecker:
    def __init__(self, words: List[str]) -> None:
        self.root = _Node()
        self.max_len = 0
        for word in words:
            if len(word) > self.max_len:
                self.max_len = len(word)
            node = self.root
            for ch in reversed(word):
                nxt = node.children.get(ch)
                if nxt is None:
                    nxt = _Node()
                    node.children[ch] = nxt
                node = nxt
            node.is_end = True
        self.stream = deque(maxlen=self.max_len)

    def query(self, letter: str) -> bool:
        self.stream.append(letter)
        node = self.root
        for ch in reversed(self.stream):
            node = node.children.get(ch)
            if node is None:
                return False
            if node.is_end:
                return True
        return False
