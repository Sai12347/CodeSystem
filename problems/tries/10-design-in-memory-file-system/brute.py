class FileSystem:
    def __init__(self) -> None:
        self.dirs = {"/"}
        self.files = {}

    def _parent(self, path: str) -> str:
        idx = path.rfind("/")
        return "/" if idx == 0 else path[:idx]

    def ls(self, path: str) -> List[str]:
        if path in self.files:
            return [path.rsplit("/", 1)[-1]]
        entries = set()
        for d in self.dirs:
            if d != "/" and self._parent(d) == path:
                entries.add(d.rsplit("/", 1)[-1])
        for f in self.files:
            if self._parent(f) == path:
                entries.add(f.rsplit("/", 1)[-1])
        return sorted(entries)

    def mkdir(self, path: str) -> None:
        parts = path.split("/")[1:]
        cur = ""
        for p in parts:
            cur += "/" + p
            self.dirs.add(cur)

    def addContentToFile(self, filePath: str, content: str) -> None:
        parent = self._parent(filePath)
        if parent != "/":
            self.mkdir(parent)
        self.files[filePath] = self.files.get(filePath, "") + content

    def readContentFromFile(self, filePath: str) -> str:
        return self.files[filePath]
