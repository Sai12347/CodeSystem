class Solution:
    def maxBalancedLength(self, fragments: List[str]) -> int:
        base_pairs = 0
        pos_group = []  # (c, o) with o >= c
        neg_group = []  # (c, o) with o < c
        for f in fragments:
            o = 0
            c = 0
            for ch in f:
                if ch == '(':
                    o += 1
                elif o > 0:
                    o -= 1
                    base_pairs += 1
                else:
                    c += 1
            if o >= c:
                pos_group.append((c, o))
            else:
                neg_group.append((c, o))
        pos_group.sort(key=lambda x: x[0])
        neg_group.sort(key=lambda x: -x[1])
        avail = 0
        cross_pairs = 0
        for c, o in pos_group + neg_group:
            m = avail if avail < c else c
            cross_pairs += m
            avail = avail - m + o
        return 2 * (base_pairs + cross_pairs)
