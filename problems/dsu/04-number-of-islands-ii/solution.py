class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        parent = [-1] * (m * n)
        rank = [0] * (m * n)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        count = 0
        ans = []
        for r, c in positions:
            idx = r * n + c
            if parent[idx] != -1:
                ans.append(count)
                continue
            parent[idx] = idx
            count += 1
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    nidx = nr * n + nc
                    if parent[nidx] != -1:
                        ra, rb = find(idx), find(nidx)
                        if ra != rb:
                            if rank[ra] < rank[rb]:
                                ra, rb = rb, ra
                            parent[rb] = ra
                            if rank[ra] == rank[rb]:
                                rank[ra] += 1
                            count -= 1
            ans.append(count)
        return ans
