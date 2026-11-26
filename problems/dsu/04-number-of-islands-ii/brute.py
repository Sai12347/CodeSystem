class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        land = set()
        ans = []
        last = 0
        for r, c in positions:
            if (r, c) in land:
                ans.append(last)
                continue
            land.add((r, c))
            seen = set()
            islands = 0
            for cell in land:
                if cell in seen:
                    continue
                islands += 1
                q = deque([cell])
                seen.add(cell)
                while q:
                    cr, cc = q.popleft()
                    for nr, nc in ((cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)):
                        nxt = (nr, nc)
                        if nxt in land and nxt not in seen:
                            seen.add(nxt)
                            q.append(nxt)
            last = islands
            ans.append(islands)
        return ans
