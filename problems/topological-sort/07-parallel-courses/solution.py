class Solution:
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        g=[[] for _ in range(n+1)];d=[0]*(n+1)
        for a,b in relations:g[a].append(b);d[b]+=1
        q=deque(i for i in range(1,n+1) if d[i]==0);sem=0;seen=0
        while q:
            sem+=1
            for _ in range(len(q)):
                u=q.popleft();seen+=1
                for v in g[u]:d[v]-=1
                for v in g[u]:
                    if d[v]==0:q.append(v)
        return sem if seen==n else -1
