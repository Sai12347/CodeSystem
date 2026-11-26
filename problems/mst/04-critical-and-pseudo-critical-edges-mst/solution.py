class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        indexed = sorted((w, u, v, i) for i, (u, v, w) in enumerate(edges))
        INF = 10**18

        def kruskal(skip_idx: int = -1, force_pos: int = -1) -> int:
            parent = list(range(n))
            size = [1] * n

            def find(x: int) -> int:
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            def union(a: int, b: int) -> bool:
                ra, rb = find(a), find(b)
                if ra == rb:
                    return False
                if size[ra] < size[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                size[ra] += size[rb]
                return True

            weight = 0
            used = 0
            if force_pos != -1:
                fw, fu, fv, _ = indexed[force_pos]
                union(fu, fv)
                weight += fw
                used += 1

            for pos, (w, u, v, idx) in enumerate(indexed):
                if idx == skip_idx or pos == force_pos:
                    continue
                if union(u, v):
                    weight += w
                    used += 1
                    if used == n - 1:
                        break

            return weight if used == n - 1 else INF

        base_mst = kruskal()
        critical = []
        pseudo = []

        for pos, (_, _, _, idx) in enumerate(indexed):
            if kruskal(skip_idx=idx) > base_mst:
                critical.append(idx)
            elif kruskal(force_pos=pos) == base_mst:
                pseudo.append(idx)

        critical.sort()
        pseudo.sort()
        return [critical, pseudo]
