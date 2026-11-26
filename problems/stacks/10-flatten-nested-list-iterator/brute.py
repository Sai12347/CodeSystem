class NestedIterator:
    def __init__(self, nestedList: List['NestedInteger']):
        # Independent eager recursive DFS flattening for cross-checking.
        self.flat = []
        self._flatten(nestedList)
        self.idx = 0

    def _flatten(self, items):
        for item in items:
            if item.isInteger():
                self.flat.append(item.getInteger())
            else:
                self._flatten(item.getList())

    def next(self) -> int:
        val = self.flat[self.idx]
        self.idx += 1
        return val

    def hasNext(self) -> bool:
        return self.idx < len(self.flat)
