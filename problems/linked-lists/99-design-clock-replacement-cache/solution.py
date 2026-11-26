class _ClockNode:
    __slots__ = ("key", "val", "ref", "prev", "next")

    def __init__(self, key: int, val: int):
        self.key = key
        self.val = val
        self.ref = 1
        self.prev: Optional[_ClockNode] = self
        self.next: Optional[_ClockNode] = self


class ClockCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.hand: Optional[_ClockNode] = None
        self.map: dict[int, _ClockNode] = {}

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        node.ref = 1
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self.map.get(key)
        if node is not None:
            node.val = value
            node.ref = 1
            return
        if len(self.map) < self.cap:
            node = _ClockNode(key, value)
            if self.hand is None:
                self.hand = node
            else:
                prev = self.hand.prev
                prev.next = node
                node.prev = prev
                node.next = self.hand
                self.hand.prev = node
            self.map[key] = node
            return
        while self.hand.ref == 1:
            self.hand.ref = 0
            self.hand = self.hand.next
        del self.map[self.hand.key]
        self.hand.key = key
        self.hand.val = value
        self.hand.ref = 1
        self.map[key] = self.hand
        self.hand = self.hand.next
