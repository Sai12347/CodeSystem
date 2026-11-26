class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        g=[[] for _ in range(numCourses)]; d=[0]*numCourses
        for a,b in prerequisites:g[b].append(a);d[a]+=1
        q=deque(i for i,x in enumerate(d) if x==0); seen=0
        while q:
            u=q.popleft();seen+=1
            for v in g[u]:
                d[v]-=1
                if d[v]==0:q.append(v)
        return seen==numCourses
