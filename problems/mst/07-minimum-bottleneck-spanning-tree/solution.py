class Solution:
    def minimumBottleneck(self, n: int, edges: List[List[int]]) -> int:
        p=list(range(n))
        def find(x):
            while p[x]!=x:p[x]=p[p[x]];x=p[x]
            return x
        if n==1:return 0
        for a,b,w in sorted(edges,key=lambda e:e[2]):
            x,y=find(a),find(b)
            if x!=y:
                p[x]=y;n-=1
                if n==1:return w
        return -1
