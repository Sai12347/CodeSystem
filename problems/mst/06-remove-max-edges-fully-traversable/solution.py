class Solution:
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        if n <= 1:
            return len(edges)

        class DSU:
            def __init__(self, size: int):
                self.parent = list(range(size + 1))
                self.sz = [1] * (size + 1)
                self.components = size

            def find(self, x: int) -> int:
                while self.parent[x] != x:
                    self.parent[x] = self.parent[self.parent[x]]
                    x = self.parent[x]
                return x

            def union(self, a: int, b: int) -> bool:
                ra, rb = self.find(a), self.find(b)
                if ra == rb:
                    return False
                if self.sz[ra] < self.sz[rb]:
                    ra, rb = rb, ra
                self.parent[rb] = ra
                self.sz[ra] += self.sz[rb]
                self.components -= 1
                return True

        alice = DSU(n)
        bob = DSU(n)
        kept = 0

        for t, u, v in edges:
            if t == 3:
                merged_a = alice.union(u, v)
                merged_b = bob.union(u, v)
                if merged_a or merged_b:
                    kept += 1

        for t, u, v in edges:
            if t == 1:
                if alice.union(u, v):
                    kept += 1
            elif t == 2:
                if bob.union(u, v):
                    kept += 1

        if alice.components != 1 or bob.components != 1:
            return -1
        return len(edges) - kept
