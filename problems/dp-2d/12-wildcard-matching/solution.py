class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        d=[False]*(len(p)+1);d[0]=True
        for j,c in enumerate(p,1):d[j]=d[j-1] and c=='*'
        for a in s:
            nd=[False]*(len(p)+1)
            for j,c in enumerate(p,1):
                if c=='*':nd[j]=nd[j-1] or d[j]
                else:nd[j]=d[j-1] and (c=='?' or c==a)
            d=nd
        return d[-1]
