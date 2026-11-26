class Solution:
    def minimumForestWeight(self, n: int, edges: List[List[int]]) -> int:
        p=list(range(n))
        def find(x):
            while p[x]!=x:p[x]=p[p[x]];x=p[x]
            return x
        total=0
        for a,b,w in sorted(edges,key=lambda e:e[2]):
            x,y=find(a),find(b)
            if x!=y:p[x]=y;total+=w
        return total
