# This is the interface that allows for creating nested lists.
# class NestedInteger:
#     def isInteger(self) -> bool:
#     def getInteger(self) -> int:
#     def getList(self) -> List['NestedInteger']:

class NestedIterator:
    def __init__(self, nestedList: List['NestedInteger']):
        self.stack = [[nestedList, 0]]
        self._next_val = None

    def next(self) -> int:
        if not self.hasNext():
            raise StopIteration()
        val = self._next_val
        self._next_val = None
        return val

    def hasNext(self) -> bool:
        if self._next_val is not None:
            return True
        while self.stack:
            lst, idx = self.stack[-1]
            if idx == len(lst):
                self.stack.pop()
                continue
            self.stack[-1][1] = idx + 1
            item = lst[idx]
            if item.isInteger():
                self._next_val = item.getInteger()
                return True
            self.stack.append([item.getList(), 0])
        return False
