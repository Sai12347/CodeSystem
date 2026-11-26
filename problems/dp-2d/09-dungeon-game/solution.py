class Solution:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        m,n=len(dungeon),len(dungeon[0]);d=[10**18]*(n+1);d[n-1]=1
        for i in range(m-1,-1,-1):
            for j in range(n-1,-1,-1):d[j]=max(1,min(d[j],d[j+1])-dungeon[i][j])
        return d[0]
