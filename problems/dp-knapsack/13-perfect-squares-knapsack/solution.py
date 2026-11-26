class Solution:
    def numSquares(self, n: int) -> int:
        d=[0]+[n+1]*n
        for x in range(1,int(n**0.5)+1):
            sq=x*x
            for s in range(sq,n+1):d[s]=min(d[s],d[s-sq]+1)
        return d[n]
