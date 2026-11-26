class Solution:
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        arr = sorted(nums)
        order = sorted(range(len(queries)), key=lambda i: queries[i][1])
        c0 = [0]
        c1 = [0]
        ans = [-1] * len(queries)
        ptr = 0
        n = len(arr)
        for qi in order:
            x, m = queries[qi]
            while ptr < n and arr[ptr] <= m:
                v = arr[ptr]
                ptr += 1
                node = 0
                for b in range(29, -1, -1):
                    if (v >> b) & 1:
                        nxt = c1[node]
                        if nxt == 0:
                            nxt = len(c0)
                            c1[node] = nxt
                            c0.append(0)
                            c1.append(0)
                        node = nxt
                    else:
                        nxt = c0[node]
                        if nxt == 0:
                            nxt = len(c0)
                            c0[node] = nxt
                            c0.append(0)
                            c1.append(0)
                        node = nxt
            if ptr == 0:
                ans[qi] = -1
            else:
                node = 0
                best = 0
                for b in range(29, -1, -1):
                    if (x >> b) & 1:
                        if c0[node]:
                            best |= 1 << b
                            node = c0[node]
                        else:
                            node = c1[node]
                    else:
                        if c1[node]:
                            best |= 1 << b
                            node = c1[node]
                        else:
                            node = c0[node]
                ans[qi] = best
        return ans
