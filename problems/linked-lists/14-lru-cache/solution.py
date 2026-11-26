class LRUCache:
    class _Node:
        __slots__ = ("key", "val", "prev", "next")

        def __init__(self, key: int = 0, val: int = 0):
            self.key = key
            self.val = val
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: "_Node") -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: "_Node") -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        self._remove(node)
        self._add_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self.map.get(key)
        if node is not None:
            node.val = value
            self._remove(node)
            self._add_front(node)
            return
        if len(self.map) == self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
        new_node = self._Node(key, value)
        self.map[key] = new_node
        self._add_front(new_node)
