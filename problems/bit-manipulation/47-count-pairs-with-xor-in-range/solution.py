class Solution:
    def countPairsXorInRange(self, nums: List[int], low: int, high: int) -> int:
        MAX_BIT = 15

        def count_less(limit: int) -> int:
            if limit <= 0:
                return 0
            c0 = [0]
            c1 = [0]
            cnt = [0]
            total = 0
            for x in nums:
                node = 0
                for b in range(MAX_BIT, -1, -1):
                    xb = (x >> b) & 1
                    lb = (limit >> b) & 1
                    if lb == 1:
                        same = c1[node] if xb == 1 else c0[node]
                        if same:
                            total += cnt[same]
                        nxt = c0[node] if xb == 1 else c1[node]
                    else:
                        nxt = c1[node] if xb == 1 else c0[node]
                    if nxt == 0:
                        break
                    node = nxt
                node = 0
                for b in range(MAX_BIT, -1, -1):
                    xb = (x >> b) & 1
                    if xb == 0:
                        if c0[node] == 0:
                            c0[node] = len(cnt)
                            c0.append(0)
                            c1.append(0)
                            cnt.append(0)
                        node = c0[node]
                    else:
                        if c1[node] == 0:
                            c1[node] = len(cnt)
                            c0.append(0)
                            c1.append(0)
                            cnt.append(0)
                        node = c1[node]
                    cnt[node] += 1
            return total

        return count_less(high + 1) - count_less(low)
