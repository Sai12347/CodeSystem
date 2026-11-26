class MinDeque:
    def __init__(self):
        self.lv = []
        self.lm = []
        self.rv = []
        self.rm = []

    def _push(self, vs, ms, val: int) -> None:
        vs.append(val)
        ms.append(val if not ms or val < ms[-1] else ms[-1])

    def _rebalance(self, src_v, src_m, dst_v, dst_m) -> None:
        m = len(src_v)
        half = (m + 1) // 2
        to_dst = src_v[:half]
        stay = src_v[half:]
        src_v.clear()
        src_m.clear()
        for x in reversed(to_dst):
            self._push(dst_v, dst_m, x)
        for x in stay:
            self._push(src_v, src_m, x)

    def pushFront(self, val: int) -> None:
        self._push(self.lv, self.lm, val)

    def pushBack(self, val: int) -> None:
        self._push(self.rv, self.rm, val)

    def popFront(self) -> int:
        if not self.lv:
            self._rebalance(self.rv, self.rm, self.lv, self.lm)
        self.lm.pop()
        return self.lv.pop()

    def popBack(self) -> int:
        if not self.rv:
            self._rebalance(self.lv, self.lm, self.rv, self.rm)
        self.rm.pop()
        return self.rv.pop()

    def getMin(self) -> int:
        if self.lm and self.rm:
            return self.lm[-1] if self.lm[-1] < self.rm[-1] else self.rm[-1]
        return self.lm[-1] if self.lm else self.rm[-1]
