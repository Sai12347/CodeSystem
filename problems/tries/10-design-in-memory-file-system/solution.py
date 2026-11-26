class _FSNode:
    __slots__ = ("children", "is_file", "content")

    def __init__(self) -> None:
        self.children = {}
        self.is_file = False
        self.content = []


class FileSystem:
    def __init__(self) -> None:
        self.root = _FSNode()

    def _traverse(self, path: str, create: bool) -> _FSNode:
        node = self.root
        if path == "/":
            return node
        for part in path.split("/")[1:]:
            nxt = node.children.get(part)
            if nxt is None:
                if not create:
                    raise KeyError(path)
                nxt = _FSNode()
                node.children[part] = nxt
            node = nxt
        return node

    def ls(self, path: str) -> List[str]:
        node = self._traverse(path, False)
        if node.is_file:
            return [path.rsplit("/", 1)[-1]]
        return sorted(node.children.keys())

    def mkdir(self, path: str) -> None:
        self._traverse(path, True)

    def addContentToFile(self, filePath: str, content: str) -> None:
        node = self._traverse(filePath, True)
        node.is_file = True
        node.content.append(content)

    def readContentFromFile(self, filePath: str) -> str:
        node = self._traverse(filePath, False)
        return "".join(node.content)
