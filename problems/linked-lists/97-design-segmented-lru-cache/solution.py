class _SNode:
    __slots__ = ("key", "val", "seg", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0, seg: int = 1):
        self.key = key
        self.val = val
        self.seg = seg
        self.prev: Optional[_SNode] = None
        self.next: Optional[_SNode] = None


class _DLL:
    def __init__(self):
        self.head = _SNode()
        self.tail = _SNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_front(self, node: _SNode) -> None:
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node
        self.size += 1

    def unlink(self, node: _SNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def pop_back(self) -> _SNode:
        node = self.tail.prev
        self.unlink(node)
        return node


class SLRUCache:
    def __init__(self, probationCap: int, protectedCap: int):
        self.prob_cap = probationCap
        self.prot_cap = protectedCap
        self.prob = _DLL()
        self.prot = _DLL()
        self.map: dict[int, _SNode] = {}

    def _promote(self, node: _SNode) -> None:
        self.prob.unlink(node)
        if self.prot.size == self.prot_cap:
            demoted = self.prot.pop_back()
            demoted.seg = 1
            self.prob.add_front(demoted)
        node.seg = 2
        self.prot.add_front(node)

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        if node.seg == 2:
            self.prot.unlink(node)
            self.prot.add_front(node)
        else:
            self._promote(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self.map.get(key)
        if node is not None:
            node.val = value
            if node.seg == 2:
                self.prot.unlink(node)
                self.prot.add_front(node)
            else:
                self._promote(node)
            return
        if self.prob.size == self.prob_cap:
            victim = self.prob.pop_back()
            del self.map[victim.key]
        node = _SNode(key, value, 1)
        self.map[key] = node
        self.prob.add_front(node)

    def segmentOf(self, key: int) -> int:
        node = self.map.get(key)
        return 0 if node is None else node.seg
