class MiddleStack:
    def __init__(self):
        self.left = deque()
        self.right = deque()

    def _rebalance(self) -> None:
        while len(self.left) > len(self.right) + 1:
            self.right.appendleft(self.left.pop())
        while len(self.left) < len(self.right):
            self.left.append(self.right.popleft())

    def push(self, val: int) -> None:
        self.right.append(val)
        self._rebalance()

    def pop(self) -> int:
        if self.right:
            v = self.right.pop()
        elif self.left:
            v = self.left.pop()
        else:
            return -1
        self._rebalance()
        return v

    def top(self) -> int:
        if self.right:
            return self.right[-1]
        return self.left[-1] if self.left else -1

    def getMiddle(self) -> int:
        return self.left[-1] if self.left else -1

    def popMiddle(self) -> int:
        if not self.left:
            return -1
        v = self.left.pop()
        self._rebalance()
        return v
