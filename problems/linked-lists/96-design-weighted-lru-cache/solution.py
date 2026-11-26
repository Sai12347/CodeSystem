class _WNode:
    __slots__ = ("key", "val", "weight", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0, weight: int = 0):
        self.key = key
        self.val = val
        self.weight = weight
        self.prev: Optional[_WNode] = None
        self.next: Optional[_WNode] = None


class WeightedLRUCache:
    def __init__(self, maxWeight: int):
        self.max_weight = maxWeight
        self.total_weight = 0
        self.map: dict[int, _WNode] = {}
        self.head = _WNode()
        self.tail = _WNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node: _WNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: _WNode) -> None:
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._add_front(node)
        return node.val

    def put(self, key: int, value: int, weight: int) -> bool:
        if weight > self.max_weight:
            return False
        old = self.map.get(key)
        if old is not None:
            self._unlink(old)
            self.total_weight -= old.weight
            del self.map[key]
        while self.total_weight + weight > self.max_weight:
            victim = self.tail.prev
            self._unlink(victim)
            self.total_weight -= victim.weight
            del self.map[victim.key]
        node = _WNode(key, value, weight)
        self.map[key] = node
        self._add_front(node)
        self.total_weight += weight
        return True

    def currentWeight(self) -> int:
        return self.total_weight
