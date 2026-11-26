class Solution:
    def makesquare(self, matchsticks: List[int]) -> bool:
        total=sum(matchsticks)
        if total%4:return False
        side=total//4;a=sorted(matchsticks,reverse=True)
        if a[0]>side:return False
        sums=[0]*4
        def dfs(i):
            if i==len(a):return True
            tried=set()
            for k in range(4):
                if sums[k] in tried or sums[k]+a[i]>side:continue
                tried.add(sums[k]);sums[k]+=a[i]
                if dfs(i+1):return True
                sums[k]-=a[i]
                if sums[k]==0:return False
            return False
        return dfs(0)
