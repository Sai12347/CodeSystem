class Solution:
    def regionsBySlashes(self, grid: List[str]) -> int:
        n = len(grid)
        total = 4 * n * n
        parent = list(range(total))
        rank = [0] * total
        components = total

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            nonlocal components
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            components -= 1

        for r in range(n):
            row = grid[r]
            for c in range(n):
                base = 4 * (r * n + c)
                ch = row[c]
                if ch == "/":
                    union(base + 0, base + 3)
                    union(base + 1, base + 2)
                elif ch == "\\":
                    union(base + 0, base + 1)
                    union(base + 2, base + 3)
                else:
                    union(base + 0, base + 1)
                    union(base + 1, base + 2)
                    union(base + 2, base + 3)

                if r + 1 < n:
                    union(base + 2, 4 * ((r + 1) * n + c) + 0)
                if c + 1 < n:
                    union(base + 1, 4 * (r * n + (c + 1)) + 3)

        return components
