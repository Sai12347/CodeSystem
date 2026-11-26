class IncrementableMinStack:
    def __init__(self, maxSize: int):
        self.cap = maxSize
        self.sz = 0
        self.mn = [0] * (4 * maxSize + 4)
        self.lazy = [0] * (4 * maxSize + 4)

    def _push_down(self, node: int) -> None:
        lz = self.lazy[node]
        if lz != 0:
            lc = node << 1
            rc = lc | 1
            self.mn[lc] += lz
            self.lazy[lc] += lz
            self.mn[rc] += lz
            self.lazy[rc] += lz
            self.lazy[node] = 0

    def _point_set(self, node: int, l: int, r: int, pos: int, val: int) -> None:
        if l == r:
            self.mn[node] = val
            self.lazy[node] = 0
            return
        self._push_down(node)
        mid = (l + r) >> 1
        if pos <= mid:
            self._point_set(node << 1, l, mid, pos, val)
        else:
            self._point_set((node << 1) | 1, mid + 1, r, pos, val)
        lc = node << 1
        a = self.mn[lc]
        b = self.mn[lc | 1]
        self.mn[node] = a if a < b else b

    def _range_add(self, node: int, l: int, r: int, ql: int, qr: int, delta: int) -> None:
        if ql <= l and r <= qr:
            self.mn[node] += delta
            self.lazy[node] += delta
            return
        self._push_down(node)
        mid = (l + r) >> 1
        if ql <= mid:
            self._range_add(node << 1, l, mid, ql, qr, delta)
        if qr > mid:
            self._range_add((node << 1) | 1, mid + 1, r, ql, qr, delta)
        lc = node << 1
        a = self.mn[lc]
        b = self.mn[lc | 1]
        self.mn[node] = a if a < b else b

    def _range_min(self, node: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql <= l and r <= qr:
            return self.mn[node]
        self._push_down(node)
        mid = (l + r) >> 1
        if qr <= mid:
            return self._range_min(node << 1, l, mid, ql, qr)
        if ql > mid:
            return self._range_min((node << 1) | 1, mid + 1, r, ql, qr)
        a = self._range_min(node << 1, l, mid, ql, qr)
        b = self._range_min((node << 1) | 1, mid + 1, r, ql, qr)
        return a if a < b else b

    def push(self, val: int) -> None:
        if self.sz == self.cap:
            return
        self._point_set(1, 0, self.cap - 1, self.sz, val)
        self.sz += 1

    def pop(self) -> int:
        res = self._range_min(1, 0, self.cap - 1, self.sz - 1, self.sz - 1)
        self.sz -= 1
        return res

    def increment(self, k: int, delta: int) -> None:
        if self.sz == 0 or k <= 0 or delta == 0:
            return
        r = (k if k < self.sz else self.sz) - 1
        self._range_add(1, 0, self.cap - 1, 0, r, delta)

    def top(self) -> int:
        return self._range_min(1, 0, self.cap - 1, self.sz - 1, self.sz - 1)

    def getMin(self) -> int:
        return self._range_min(1, 0, self.cap - 1, 0, self.sz - 1)
