class Solution:
    def sumOfDistancesInTree(self, n: int, edges: List[List[int]]) -> List[int]:
        g=[[] for _ in range(n)]
        for a,b in edges:g[a].append(b);g[b].append(a)
        parent=[-1]*n;order=[0]
        for u in order:
            for v in g[u]:
                if v!=parent[u]:parent[v]=u;order.append(v)
        size=[1]*n;ans=[0]*n
        for u in reversed(order[1:]):
            p=parent[u];size[p]+=size[u];ans[p]+=ans[u]+size[u]
        for u in order[1:]:ans[u]=ans[parent[u]]-size[u]+n-size[u]
        return ans
