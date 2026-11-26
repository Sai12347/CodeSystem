import heapq


class _TTLNode:
    __slots__ = ("key", "val", "exp", "ver", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0, exp: int = 0, ver: int = 0):
        self.key = key
        self.val = val
        self.exp = exp
        self.ver = ver
        self.prev: "_TTLNode | None" = None
        self.next: "_TTLNode | None" = None


class TTLLRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map: dict[int, _TTLNode] = {}
        self.heap: list[tuple[int, int, int]] = []
        self.ver = 0
        self.head = _TTLNode()
        self.tail = _TTLNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node: _TTLNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node: _TTLNode) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _purge(self, timestamp: int) -> None:
        while self.heap and self.heap[0][0] <= timestamp:
            _, ver, key = heapq.heappop(self.heap)
            node = self.map.get(key)
            if node is not None and node.ver == ver:
                self._unlink(node)
                del self.map[key]

    def get(self, key: int, timestamp: int) -> int:
        self._purge(timestamp)
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._insert_front(node)
        return node.val

    def put(self, key: int, value: int, timestamp: int, ttl: int) -> None:
        self._purge(timestamp)
        self.ver += 1
        exp = timestamp + ttl
        node = self.map.get(key)
        if node is not None:
            node.val = value
            node.exp = exp
            node.ver = self.ver
            self._unlink(node)
            self._insert_front(node)
        else:
            if len(self.map) == self.cap:
                lru = self.tail.prev
                self._unlink(lru)
                del self.map[lru.key]
            node = _TTLNode(key, value, exp, self.ver)
            self._insert_front(node)
            self.map[key] = node
        heapq.heappush(self.heap, (exp, self.ver, key))
