class LFUCache:
    class _Node:
        __slots__ = ("key", "val", "freq", "prev", "next")

        def __init__(self, key: int = 0, val: int = 0):
            self.key = key
            self.val = val
            self.freq = 1
            self.prev = None
            self.next = None

    class _DLL:
        __slots__ = ("head", "tail", "size")

        def __init__(self):
            self.head = LFUCache._Node()
            self.tail = LFUCache._Node()
            self.head.next = self.tail
            self.tail.prev = self.head
            self.size = 0

        def add_front(self, node: "LFUCache._Node") -> None:
            node.prev = self.head
            node.next = self.head.next
            self.head.next.prev = node
            self.head.next = node
            self.size += 1

        def remove(self, node: "LFUCache._Node") -> None:
            node.prev.next = node.next
            node.next.prev = node.prev
            self.size -= 1

        def pop_back(self) -> "LFUCache._Node":
            node = self.tail.prev
            self.remove(node)
            return node

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_map = {}
        self.freq_map = {}
        self.min_freq = 0

    def _touch(self, node: "_Node") -> None:
        freq = node.freq
        bucket = self.freq_map[freq]
        bucket.remove(node)
        if bucket.size == 0:
            del self.freq_map[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        node.freq += 1
        if node.freq not in self.freq_map:
            self.freq_map[node.freq] = self._DLL()
        self.freq_map[node.freq].add_front(node)

    def get(self, key: int) -> int:
        node = self.key_map.get(key)
        if node is None:
            return -1
        self._touch(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        node = self.key_map.get(key)
        if node is not None:
            node.val = value
            self._touch(node)
            return
        if len(self.key_map) == self.capacity:
            min_bucket = self.freq_map[self.min_freq]
            evicted = min_bucket.pop_back()
            if min_bucket.size == 0:
                del self.freq_map[self.min_freq]
            del self.key_map[evicted.key]
        new_node = self._Node(key, value)
        self.key_map[key] = new_node
        self.min_freq = 1
        if 1 not in self.freq_map:
            self.freq_map[1] = self._DLL()
        self.freq_map[1].add_front(new_node)
