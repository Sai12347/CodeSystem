class Solution:
    def numSimilarGroups(self, strs: List[str]) -> int:
        n = len(strs)
        parent = list(range(n))
        rank = [0] * n
        groups = n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def is_similar(a: str, b: str) -> bool:
            diff = 0
            for ca, cb in zip(a, b):
                if ca != cb:
                    diff += 1
                    if diff > 2:
                        return False
            return True

        for i in range(n):
            si = strs[i]
            for j in range(i + 1, n):
                ri, rj = find(i), find(j)
                if ri != rj and is_similar(si, strs[j]):
                    if rank[ri] < rank[rj]:
                        ri, rj = rj, ri
                    parent[rj] = ri
                    if rank[ri] == rank[rj]:
                        rank[ri] += 1
                    groups -= 1

        return groups
