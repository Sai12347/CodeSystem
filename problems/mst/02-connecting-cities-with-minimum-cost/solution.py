class Solution:
    def minimumCost(self, n: int, connections: List[List[int]]) -> int:
        if n <= 1:
            return 0
        if len(connections) < n - 1:
            return -1

        parent = list(range(n + 1))
        size = [1] * (n + 1)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        sorted_edges = sorted(connections, key=lambda e: e[2])
        total = 0
        components = n

        for u, v, cost in sorted_edges:
            ru, rv = find(u), find(v)
            if ru != rv:
                if size[ru] < size[rv]:
                    ru, rv = rv, ru
                parent[rv] = ru
                size[ru] += size[rv]
                total += cost
                components -= 1
                if components == 1:
                    return total

        return -1
