class Solution:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        n=len(graph);rev=[[] for _ in range(n)];out=[len(x) for x in graph]
        for u,row in enumerate(graph):
            for v in row:rev[v].append(u)
        q=deque(i for i,x in enumerate(out) if x==0);safe=[]
        while q:
            v=q.popleft();safe.append(v)
            for u in rev[v]:
                out[u]-=1
                if out[u]==0:q.append(u)
        return sorted(safe)
