class Solution:
    def minimaxPathQueries(self, n: int, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        inf=10**18;d=[[inf]*n for _ in range(n)]
        for i in range(n):d[i][i]=0
        for a,b,w in edges:d[a][b]=d[b][a]=min(d[a][b],w)
        for k in range(n):
            for i in range(n):
                for j in range(n):d[i][j]=min(d[i][j],max(d[i][k],d[k][j]))
        return [-1 if d[a][b]==inf else d[a][b] for a,b in queries]
