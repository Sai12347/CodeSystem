class Solution:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        edges = [(wells[i], 0, i + 1) for i in range(n)]
        for u, v, cost in pipes:
            edges.append((cost, u, v))
        edges.sort()

        parent = list(range(n + 1))
        size = [1] * (n + 1)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        total = 0
        components = n + 1
        for cost, u, v in edges:
            ru, rv = find(u), find(v)
            if ru != rv:
                if size[ru] < size[rv]:
                    ru, rv = rv, ru
                parent[rv] = ru
                size[ru] += size[rv]
                total += cost
                components -= 1
                if components == 1:
                    break
        return total
