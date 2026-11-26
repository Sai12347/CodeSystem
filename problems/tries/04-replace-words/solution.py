class _TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children = {}
        self.is_end = False


class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        root = _TrieNode()
        for word in dictionary:
            node = root
            for ch in word:
                nxt = node.children.get(ch)
                if nxt is None:
                    nxt = _TrieNode()
                    node.children[ch] = nxt
                node = nxt
            node.is_end = True

        result = []
        for token in sentence.split(" "):
            node = root
            replacement = token
            for i, ch in enumerate(token):
                node = node.children.get(ch)
                if node is None:
                    break
                if node.is_end:
                    replacement = token[:i + 1]
                    break
            result.append(replacement)
        return " ".join(result)
