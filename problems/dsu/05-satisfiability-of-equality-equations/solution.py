class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        parent = list(range(26))
        rank = [0] * 26

        def find(x: int) -> int:
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

        for eq in equations:
            if eq[1] == "=":
                union(ord(eq[0]) - 97, ord(eq[3]) - 97)

        for eq in equations:
            if eq[1] == "!":
                if find(ord(eq[0]) - 97) == find(ord(eq[3]) - 97):
                    return False
        return True
