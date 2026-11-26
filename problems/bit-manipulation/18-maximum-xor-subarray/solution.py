class Solution:
    def maxXorSubarray(self, nums: List[int]) -> int:
        c0 = [-1]
        c1 = [-1]

        def insert(val: int) -> None:
            node = 0
            for b in range(29, -1, -1):
                bit = (val >> b) & 1
                if bit == 0:
                    nxt = c0[node]
                    if nxt == -1:
                        nxt = len(c0)
                        c0[node] = nxt
                        c0.append(-1)
                        c1.append(-1)
                    node = nxt
                else:
                    nxt = c1[node]
                    if nxt == -1:
                        nxt = len(c0)
                        c1[node] = nxt
                        c0.append(-1)
                        c1.append(-1)
                    node = nxt

        def query(val: int) -> int:
            node = 0
            res = 0
            for b in range(29, -1, -1):
                bit = (val >> b) & 1
                if bit == 0:
                    if c1[node] != -1:
                        res |= 1 << b
                        node = c1[node]
                    else:
                        node = c0[node]
                else:
                    if c0[node] != -1:
                        res |= 1 << b
                        node = c0[node]
                    else:
                        node = c1[node]
            return res

        insert(0)
        pref = 0
        best = 0
        for x in nums:
            pref ^= x
            cand = query(pref)
            if cand > best:
                best = cand
            insert(pref)
        return best
