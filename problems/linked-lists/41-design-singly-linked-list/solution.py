class MyLinkedList:
    class _Node:
        __slots__ = ("val", "prev", "next")

        def __init__(self, val: int = 0):
            self.val = val
            self.prev = None
            self.next = None

    def __init__(self):
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _node_at(self, index: int) -> "_Node":
        if index < self.size // 2:
            curr = self.head.next
            for _ in range(index):
                curr = curr.next
        else:
            curr = self.tail.prev
            for _ in range(self.size - 1 - index):
                curr = curr.prev
        return curr

    def _insert_before(self, target: "_Node", val: int) -> None:
        node = self._Node(val)
        prev = target.prev
        prev.next = node
        node.prev = prev
        node.next = target
        target.prev = node
        self.size += 1

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1
        return self._node_at(index).val

    def addAtHead(self, val: int) -> None:
        self._insert_before(self.head.next, val)

    def addAtTail(self, val: int) -> None:
        self._insert_before(self.tail, val)

    def addAtIndex(self, index: int, val: int) -> None:
        if index < 0 or index > self.size:
            return
        if index == self.size:
            self._insert_before(self.tail, val)
        else:
            self._insert_before(self._node_at(index), val)

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return
        node = self._node_at(index)
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
