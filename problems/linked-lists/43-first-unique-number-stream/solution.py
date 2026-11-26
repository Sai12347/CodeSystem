class FirstUnique:
    class _Node:
        __slots__ = ("val", "prev", "next")

        def __init__(self, val: int = 0):
            self.val = val
            self.prev = None
            self.next = None

    def __init__(self, nums: List[int]):
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.nodes = {}
        for x in nums:
            self.add(x)

    def _append(self, node: "_Node") -> None:
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node

    def _remove(self, node: "_Node") -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def showFirstUnique(self) -> int:
        if self.head.next is self.tail:
            return -1
        return self.head.next.val

    def add(self, value: int) -> None:
        if value not in self.nodes:
            node = self._Node(value)
            self._append(node)
            self.nodes[value] = node
        else:
            existing = self.nodes[value]
            if existing is not None:
                self._remove(existing)
                self.nodes[value] = None
