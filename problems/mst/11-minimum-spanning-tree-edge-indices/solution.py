class Solution:
    def minimumSpanningTreeEdges(self, n: int, edges: List[List[int]]) -> List[int]:
        p=list(range(n))
        def find(x):
            while p[x]!=x:p[x]=p[p[x]];x=p[x]
            return x
        chosen=[]
        for i in sorted(range(len(edges)),key=lambda i:(edges[i][2],i)):
            a,b,w=edges[i];x,y=find(a),find(b)
            if x!=y:p[x]=y;chosen.append(i)
        return sorted(chosen) if len(chosen)==n-1 else []
