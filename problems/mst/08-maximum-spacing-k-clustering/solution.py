class Solution:
    def maximumSpacing(self, n: int, k: int, edges: List[List[int]]) -> int:
        if k<=1 or n<=1:return -1
        p=list(range(n));components=n
        def find(x):
            while p[x]!=x:p[x]=p[p[x]];x=p[x]
            return x
        for a,b,w in sorted(edges,key=lambda e:e[2]):
            x,y=find(a),find(b)
            if x!=y:
                if components==k:return w
                p[x]=y;components-=1
        return -1
