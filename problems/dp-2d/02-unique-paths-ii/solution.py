class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        d=[0]*len(obstacleGrid[0]);d[0]=1
        for row in obstacleGrid:
            for j,x in enumerate(row):
                if x:d[j]=0
                elif j:d[j]+=d[j-1]
        return d[-1]
