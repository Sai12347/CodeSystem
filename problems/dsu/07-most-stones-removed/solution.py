class Solution:
    def removeStones(self, stones: List[List[int]]) -> int:
        parent = {}
        rank = {}

        def find(x: int) -> int:
            if x not in parent:
                parent[x] = x
                rank[x] = 0
                return x
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1

        OFFSET = 10001
        for r, c in stones:
            union(r, c + OFFSET)

        roots = {find(node) for node in parent}
        return len(stones) - len(roots)
