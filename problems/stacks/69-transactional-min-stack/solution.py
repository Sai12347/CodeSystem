class TransactionalStack:
    def __init__(self):
        self.st = []  # (val, running_min)
        self.tx = []  # list of [head, tail] where node is [is_push_undo, val, next]

    def _raw_push(self, val: int) -> None:
        mn = val if not self.st or val < self.st[-1][1] else self.st[-1][1]
        self.st.append((val, mn))

    def _raw_pop(self) -> int:
        return self.st.pop()[0]

    def _record(self, is_push_undo: bool, val: int) -> None:
        if self.tx:
            frame = self.tx[-1]
            node = [is_push_undo, val, frame[0]]
            frame[0] = node
            if frame[1] is None:
                frame[1] = node

    def push(self, val: int) -> None:
        self._raw_push(val)
        self._record(False, 0)  # undo push by popping

    def pop(self) -> int:
        val = self._raw_pop()
        self._record(True, val)  # undo pop by pushing val
        return val

    def top(self) -> int:
        return self.st[-1][0]

    def getMin(self) -> int:
        return self.st[-1][1]

    def begin(self) -> None:
        self.tx.append([None, None])

    def rollback(self) -> bool:
        if not self.tx:
            return False
        cur = self.tx.pop()[0]
        while cur is not None:
            if cur[0]:
                self._raw_push(cur[1])
            else:
                self._raw_pop()
            cur = cur[2]
        return True

    def commit(self) -> bool:
        if not self.tx:
            return False
        child = self.tx.pop()
        if self.tx and child[0] is not None:
            parent = self.tx[-1]
            child[1][2] = parent[0]
            parent[0] = child[0]
            if parent[1] is None:
                parent[1] = child[1]
        return True
