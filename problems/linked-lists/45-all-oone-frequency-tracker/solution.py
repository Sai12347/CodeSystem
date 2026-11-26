class AllOneTracker:
    class _Bucket:
        __slots__ = ("count", "keys", "prev", "next")

        def __init__(self, count: int = 0):
            self.count = count
            self.keys = set()
            self.prev = None
            self.next = None

    def __init__(self):
        self.head = self._Bucket(0)
        self.tail = self._Bucket(0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.key_map = {}

    def _insert_after(self, prev: "_Bucket", count: int) -> "_Bucket":
        node = self._Bucket(count)
        nxt = prev.next
        prev.next = node
        node.prev = prev
        node.next = nxt
        nxt.prev = node
        return node

    def _remove_if_empty(self, node: "_Bucket") -> None:
        if not node.keys:
            node.prev.next = node.next
            node.next.prev = node.prev

    def inc(self, key: str) -> None:
        if key not in self.key_map:
            if self.head.next is self.tail or self.head.next.count != 1:
                target = self._insert_after(self.head, 1)
            else:
                target = self.head.next
            target.keys.add(key)
            self.key_map[key] = target
            return
        cur = self.key_map[key]
        nxt_cnt = cur.count + 1
        if cur.next is self.tail or cur.next.count != nxt_cnt:
            target = self._insert_after(cur, nxt_cnt)
        else:
            target = cur.next
        target.keys.add(key)
        self.key_map[key] = target
        cur.keys.remove(key)
        self._remove_if_empty(cur)

    def dec(self, key: str) -> None:
        if key not in self.key_map:
            return
        cur = self.key_map[key]
        if cur.count == 1:
            del self.key_map[key]
        else:
            prv_cnt = cur.count - 1
            if cur.prev is self.head or cur.prev.count != prv_cnt:
                target = self._insert_after(cur.prev, prv_cnt)
            else:
                target = cur.prev
            target.keys.add(key)
            self.key_map[key] = target
        cur.keys.remove(key)
        self._remove_if_empty(cur)

    def getMaxCount(self) -> int:
        if self.head.next is self.tail:
            return 0
        return self.tail.prev.count

    def getMinCount(self) -> int:
        if self.head.next is self.tail:
            return 0
        return self.head.next.count

    def getCount(self, key: str) -> int:
        b = self.key_map.get(key)
        return 0 if b is None else b.count
