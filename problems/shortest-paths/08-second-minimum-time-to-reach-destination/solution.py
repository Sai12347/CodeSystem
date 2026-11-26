class Solution:
    def secondMinimum(self, n: int, edges: List[List[int]], time: int, change: int) -> int:
        g=[[] for _ in range(n+1)]
        for a,b in edges:g[a].append(b);g[b].append(a)
        first=[-1]*(n+1);second=[-1]*(n+1);q=deque([(1,0)]);first[1]=0;steps=None
        while q:
            u,d=q.popleft()
            for v in g[u]:
                nd=d+1
                if first[v]<0:first[v]=nd;q.append((v,nd))
                elif second[v]<0 and nd>first[v]:
                    second[v]=nd
                    if v==n:steps=nd;break
                    q.append((v,nd))
            if steps is not None:break
        cur=0
        for _ in range(steps):
            if (cur//change)%2:cur=((cur//change)+1)*change
            cur+=time
        return cur
