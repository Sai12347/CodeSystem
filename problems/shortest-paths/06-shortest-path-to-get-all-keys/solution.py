class Solution:
    def shortestPathAllKeys(self, grid: List[str]) -> int:
        m, n = len(grid), len(grid[0])
        sr = sc = 0
        key_count = 0

        for r in range(m):
            for c in range(n):
                ch = grid[r][c]
                if ch == "@":
                    sr, sc = r, c
                elif "a" <= ch <= "f":
                    key_count += 1

        target_mask = (1 << key_count) - 1
        visited = {(sr, sc, 0)}
        q = deque([(sr, sc, 0, 0)])

        while q:
            r, c, mask, steps = q.popleft()
            ns = steps + 1
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if not (0 <= nr < m and 0 <= nc < n):
                    continue
                ch = grid[nr][nc]
                if ch == "#":
                    continue
                if "A" <= ch <= "F" and not (mask & (1 << (ord(ch) - ord("A")))):
                    continue
                nmask = mask
                if "a" <= ch <= "f":
                    nmask |= 1 << (ord(ch) - ord("a"))
                    if nmask == target_mask:
                        return ns
                state = (nr, nc, nmask)
                if state not in visited:
                    visited.add(state)
                    q.append((nr, nc, nmask, ns))

        return -1
