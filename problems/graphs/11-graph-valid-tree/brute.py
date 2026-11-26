class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # Independent Union-Find check: must have no cycles and end with 1 component
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        components = n
        for u, v in edges:
            ru, rv = find(u), find(v)
            if ru == rv:
                return False
            parent[ru] = rv
            components -= 1

        return components == 1
