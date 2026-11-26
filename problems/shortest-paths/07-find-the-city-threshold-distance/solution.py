class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        inf=10**9;d=[[inf]*n for _ in range(n)]
        for i in range(n):d[i][i]=0
        for a,b,w in edges:d[a][b]=d[b][a]=w
        for k in range(n):
            for i in range(n):
                for j in range(n):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
        return min(range(n),key=lambda i:(sum(x<=distanceThreshold for j,x in enumerate(d[i]) if j!=i),-i))
