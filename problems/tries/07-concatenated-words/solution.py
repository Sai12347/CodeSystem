class _TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children = {}
        self.is_end = False


class Solution:
    def findAllConcatenatedWordsInADict(self, words: List[str]) -> List[str]:
        root = _TrieNode()
        result: List[str] = []

        def can_form(word: str) -> bool:
            n = len(word)
            visited = [False] * (n + 1)

            def dfs(start: int) -> bool:
                if start == n:
                    return True
                if visited[start]:
                    return False
                visited[start] = True
                node = root
                for i in range(start, n):
                    node = node.children.get(word[i])
                    if node is None:
                        break
                    if node.is_end and dfs(i + 1):
                        return True
                return False

            return dfs(0)

        def insert(word: str) -> None:
            node = root
            for ch in word:
                nxt = node.children.get(ch)
                if nxt is None:
                    nxt = _TrieNode()
                    node.children[ch] = nxt
                node = nxt
            node.is_end = True

        for w in sorted(words, key=len):
            if not w:
                continue
            if can_form(w):
                result.append(w)
            else:
                insert(w)

        return result
