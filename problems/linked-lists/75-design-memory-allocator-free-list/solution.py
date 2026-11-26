class _SegNode:
    __slots__ = ("start", "length", "mid", "prev", "next")

    def __init__(self, start: int = 0, length: int = 0, mid: int = 0):
        self.start = start
        self.length = length
        self.mid = mid
        self.prev: "_SegNode | None" = None
        self.next: "_SegNode | None" = None


class MemoryAllocator:
    def __init__(self, n: int):
        self.head = _SegNode()
        self.tail = _SegNode()
        first = _SegNode(0, n, 0)
        self.head.next = first
        first.prev = self.head
        first.next = self.tail
        self.tail.prev = first
        self.owned: dict[int, list[_SegNode]] = {}

    def _unlink(self, node: _SegNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_before(self, ref: _SegNode, node: _SegNode) -> None:
        node.prev = ref.prev
        node.next = ref
        ref.prev.next = node
        ref.prev = node

    def allocate(self, size: int, mID: int) -> int:
        curr = self.head.next
        while curr is not self.tail:
            if curr.mid == 0 and curr.length >= size:
                addr = curr.start
                if curr.length == size:
                    curr.mid = mID
                    alloc = curr
                else:
                    alloc = _SegNode(addr, size, mID)
                    curr.start += size
                    curr.length -= size
                    self._insert_before(curr, alloc)
                self.owned.setdefault(mID, []).append(alloc)
                return addr
            curr = curr.next
        return -1

    def freeMemory(self, mID: int) -> int:
        nodes = self.owned.pop(mID, None)
        if not nodes:
            return 0
        freed = 0
        for node in nodes:
            freed += node.length
            node.mid = 0
            if node.prev is not self.head and node.prev.mid == 0:
                left = node.prev
                node.start = left.start
                node.length += left.length
                self._unlink(left)
            if node.next is not self.tail and node.next.mid == 0:
                right = node.next
                node.length += right.length
                self._unlink(right)
        return freed
