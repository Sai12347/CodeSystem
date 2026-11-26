class Solution:
    def shortestPathAllKeys(self, grid: List[str]) -> int:
        # Independent cross-check: compressed-graph Dijkstra over (poi_idx, key_mask)
        m, n = len(grid), len(grid[0])
        poi = {}
        key_count = 0
        for r in range(m):
            for c in range(n):
                ch = grid[r][c]
                if ch == "@":
                    poi["@"] = (r, c)
                elif "a" <= ch <= "f":
                    poi[ch] = (r, c)
                    key_count += 1

        target = (1 << key_count) - 1
        bfs_cache = {}

        def reach_keys(src_ch: str, mask: int):
            key = (src_ch, mask)
            if key in bfs_cache:
                return bfs_cache[key]
            sr, sc = poi[src_ch]
            seen = [[False] * n for _ in range(m)]
            seen[sr][sc] = True
            q = deque([(sr, sc, 0)])
            found = []
            while q:
                r, c, d = q.popleft()
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if not (0 <= nr < m and 0 <= nc < n) or seen[nr][nc]:
                        continue
                    ch = grid[nr][nc]
                    if ch == "#":
                        continue
                    if "A" <= ch <= "F" and not (mask & (1 << (ord(ch) - ord("A")))):
                        continue
                    seen[nr][nc] = True
                    if "a" <= ch <= "f" and not (mask & (1 << (ord(ch) - ord("a")))):
                        found.append((ch, d + 1))
                    else:
                        q.append((nr, nc, d + 1))
            bfs_cache[key] = found
            return found

        dist = {("@", 0): 0}
        heap = [(0, "@", 0)]
        while heap:
            d, cur, mask = heapq.heappop(heap)
            if d > dist[(cur, mask)]:
                continue
            if mask == target:
                return d
            for nxt_k, w in reach_keys(cur, mask):
                nmask = mask | (1 << (ord(nxt_k) - ord("a")))
                nd = d + w
                state = (nxt_k, nmask)
                if nd < dist.get(state, 10**9):
                    dist[state] = nd
                    heapq.heappush(heap, (nd, nxt_k, nmask))
        return -1
