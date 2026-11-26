class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n<=2:return list(range(n))
        g=[set() for _ in range(n)]
        for a,b in edges:g[a].add(b);g[b].add(a)
        leaves=[i for i in range(n) if len(g[i])==1];left=n
        while left>2:
            left-=len(leaves); nxt=[]
            for u in leaves:
                v=g[u].pop();g[v].remove(u)
                if len(g[v])==1:nxt.append(v)
            leaves=nxt
        return sorted(leaves)
