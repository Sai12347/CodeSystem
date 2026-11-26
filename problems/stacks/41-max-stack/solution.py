class MaxStack:
    def __init__(self):
        self.stack = []
        self.heap = []
        self.removed = set()
        self.next_id = 0

    def _clean_stack(self) -> None:
        while self.stack and self.stack[-1][1] in self.removed:
            self.stack.pop()

    def _clean_heap(self) -> None:
        while self.heap and -self.heap[0][1] in self.removed:
            heapq.heappop(self.heap)

    def push(self, x: int) -> None:
        uid = self.next_id
        self.next_id += 1
        self.stack.append((x, uid))
        heapq.heappush(self.heap, (-x, -uid))

    def pop(self) -> int:
        self._clean_stack()
        val, uid = self.stack.pop()
        self.removed.add(uid)
        return val

    def top(self) -> int:
        self._clean_stack()
        return self.stack[-1][0]

    def peekMax(self) -> int:
        self._clean_heap()
        return -self.heap[0][0]

    def popMax(self) -> int:
        self._clean_heap()
        neg_val, neg_uid = heapq.heappop(self.heap)
        self.removed.add(-neg_uid)
        return -neg_val
