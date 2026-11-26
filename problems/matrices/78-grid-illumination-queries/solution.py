class Solution:
    def gridIllumination(self, n: int, lamps: List[List[int]], queries: List[List[int]]) -> List[int]:
        active = set()
        rows = defaultdict(int)
        cols = defaultdict(int)
        d1 = defaultdict(int)
        d2 = defaultdict(int)
        for r, c in lamps:
            if (r, c) not in active:
                active.add((r, c))
                rows[r] += 1
                cols[c] += 1
                d1[r - c] += 1
                d2[r + c] += 1

        ans = []
        for qr, qc in queries:
            if rows[qr] > 0 or cols[qc] > 0 or d1[qr - qc] > 0 or d2[qr + qc] > 0:
                ans.append(1)
            else:
                ans.append(0)
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = qr + dr, qc + dc
                    if (nr, nc) in active:
                        active.remove((nr, nc))
                        rows[nr] -= 1
                        cols[nc] -= 1
                        d1[nr - nc] -= 1
                        d2[nr + nc] -= 1
        return ans
