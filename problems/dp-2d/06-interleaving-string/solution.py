class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s1)+len(s2)!=len(s3):return False
        d=[False]*(len(s2)+1);d[0]=True
        for j in range(1,len(s2)+1):d[j]=d[j-1] and s2[j-1]==s3[j-1]
        for i,a in enumerate(s1,1):
            d[0]=d[0] and a==s3[i-1]
            for j,b in enumerate(s2,1):d[j]=(d[j] and a==s3[i+j-1]) or (d[j-1] and b==s3[i+j-1])
        return d[-1]
