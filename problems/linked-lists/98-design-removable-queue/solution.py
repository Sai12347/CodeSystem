class _QNode:
    __slots__ = ("val", "prev", "next")

    def __init__(self, val: int = 0):
        self.val = val
        self.prev: Optional[_QNode] = None
        self.next: Optional[_QNode] = None


class RemovableQueue:
    def __init__(self):
        self.head = _QNode()
        self.tail = _QNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.map: dict[int, _QNode] = {}

    def _unlink(self, node: _QNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def enqueue(self, id: int) -> bool:
        if id in self.map:
            return False
        node = _QNode(id)
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node
        self.map[id] = node
        return True

    def dequeue(self) -> int:
        if not self.map:
            return -1
        node = self.head.next
        self._unlink(node)
        del self.map[node.val]
        return node.val

    def cancel(self, id: int) -> bool:
        node = self.map.pop(id, None)
        if node is None:
            return False
        self._unlink(node)
        return True

    def peekFront(self) -> int:
        if not self.map:
            return -1
        return self.head.next.val

    def size(self) -> int:
        return len(self.map)
