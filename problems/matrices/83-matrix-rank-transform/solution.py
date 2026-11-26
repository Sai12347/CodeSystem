class Solution:
    def matrixRankTransform(self, matrix: List[List[int]]) -> List[List[int]]:
        m, n = len(matrix), len(matrix[0])
        groups = defaultdict(list)
        for r in range(m):
            for c in range(n):
                groups[matrix[r][c]].append((r, c))

        row_max = [0] * m
        col_max = [0] * n
        ans = [[0] * n for _ in range(m)]

        for val in sorted(groups):
            parent = {}

            def find(x: int) -> int:
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            cells = groups[val]
            for r, c in cells:
                cc = m + c
                if r not in parent:
                    parent[r] = r
                if cc not in parent:
                    parent[cc] = cc
                ra, rb = find(r), find(cc)
                if ra != rb:
                    parent[ra] = rb

            comp_rank = {}
            for r, c in cells:
                root = find(r)
                prev = row_max[r] if row_max[r] > col_max[c] else col_max[c]
                if root not in comp_rank or prev > comp_rank[root]:
                    comp_rank[root] = prev

            for r, c in cells:
                rank = comp_rank[find(r)] + 1
                ans[r][c] = rank
                row_max[r] = rank
                col_max[c] = rank
        return ans
