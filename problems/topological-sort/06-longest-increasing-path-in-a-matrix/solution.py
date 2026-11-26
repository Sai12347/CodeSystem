class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        m,n=len(matrix),len(matrix[0]);ind=[[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
                    x,y=i+di,j+dj
                    if 0<=x<m and 0<=y<n and matrix[x][y]<matrix[i][j]:ind[i][j]+=1
        q=deque((i,j) for i in range(m) for j in range(n) if ind[i][j]==0);length=0
        while q:
            length+=1
            for _ in range(len(q)):
                i,j=q.popleft()
                for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
                    x,y=i+di,j+dj
                    if 0<=x<m and 0<=y<n and matrix[x][y]>matrix[i][j]:
                        ind[x][y]-=1
                        if ind[x][y]==0:q.append((x,y))
        return length
