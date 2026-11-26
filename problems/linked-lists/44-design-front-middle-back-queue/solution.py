class FrontMiddleBackQueue:
    def __init__(self):
        self.left = deque()
        self.right = deque()

    def _rebalance(self) -> None:
        if len(self.left) > len(self.right) + 1:
            self.right.appendleft(self.left.pop())
        elif len(self.left) < len(self.right):
            self.left.append(self.right.popleft())

    def pushFront(self, val: int) -> None:
        self.left.appendleft(val)
        self._rebalance()

    def pushMiddle(self, val: int) -> None:
        if len(self.left) > len(self.right):
            self.right.appendleft(self.left.pop())
        self.left.append(val)

    def pushBack(self, val: int) -> None:
        self.right.append(val)
        self._rebalance()

    def popFront(self) -> int:
        if not self.left:
            return -1
        val = self.left.popleft()
        self._rebalance()
        return val

    def popMiddle(self) -> int:
        if not self.left:
            return -1
        val = self.left.pop()
        self._rebalance()
        return val

    def popBack(self) -> int:
        if not self.left:
            return -1
        if not self.right:
            return self.left.pop()
        val = self.right.pop()
        self._rebalance()
        return val
