class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        g=[[] for _ in range(numCourses)];d=[0]*numCourses
        for a,b in prerequisites:g[b].append(a);d[a]+=1
        q=[i for i,x in enumerate(d) if x==0];heapq.heapify(q);out=[]
        while q:
            u=heapq.heappop(q);out.append(u)
            for v in g[u]:
                d[v]-=1
                if d[v]==0:heapq.heappush(q,v)
        return out if len(out)==numCourses else []
