class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        d=[0]*(len(t)+1);d[0]=1
        for a in s:
            for j in range(len(t)-1,-1,-1):
                if a==t[j]:d[j+1]+=d[j]
        return d[-1]
