class _PinNode:
    __slots__ = ("key", "val", "pinned", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.pinned = False
        self.prev: Optional[_PinNode] = None
        self.next: Optional[_PinNode] = None


class PinnedLRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map: dict[int, _PinNode] = {}
        self.head = _PinNode()
        self.tail = _PinNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node: _PinNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None

    def _add_front(self, node: _PinNode) -> None:
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        if not node.pinned:
            self._unlink(node)
            self._add_front(node)
        return node.val

    def put(self, key: int, value: int) -> bool:
        node = self.map.get(key)
        if node is not None:
            node.val = value
            if not node.pinned:
                self._unlink(node)
                self._add_front(node)
            return True
        if len(self.map) == self.cap:
            if self.tail.prev is self.head:
                return False
            victim = self.tail.prev
            self._unlink(victim)
            del self.map[victim.key]
        node = _PinNode(key, value)
        self.map[key] = node
        self._add_front(node)
        return True

    def pin(self, key: int) -> bool:
        node = self.map.get(key)
        if node is None:
            return False
        if not node.pinned:
            self._unlink(node)
            node.pinned = True
        return True

    def unpin(self, key: int) -> bool:
        node = self.map.get(key)
        if node is None:
            return False
        if node.pinned:
            node.pinned = False
            self._add_front(node)
        return True
