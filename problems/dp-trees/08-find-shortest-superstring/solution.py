class Solution:
    def shortestSuperstring(self, words: List[str]) -> str:
        n=len(words);ov=[[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i!=j:
                    for k in range(min(len(words[i]),len(words[j])),0,-1):
                        if words[i].endswith(words[j][:k]):ov[i][j]=k;break
        dp=[[None]*n for _ in range(1<<n)]
        for i in range(n):dp[1<<i][i]=words[i]
        for mask in range(1<<n):
            for i in range(n):
                cur=dp[mask][i]
                if cur is None:continue
                for j in range(n):
                    if mask>>j&1:continue
                    m=mask|1<<j;cand=cur+words[j][ov[i][j]:];old=dp[m][j]
                    if old is None or (len(cand),cand)<(len(old),old):dp[m][j]=cand
        return min((x for x in dp[-1] if x is not None),key=lambda x:(len(x),x))

