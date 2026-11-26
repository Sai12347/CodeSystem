class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        p=[0]
        for x in nums:p.append(p[-1]+x)
        def sort_count(a):
            if len(a)<=1:return a,0
            m=len(a)//2;l,c1=sort_count(a[:m]);r,c2=sort_count(a[m:]);ans=c1+c2;j=k=0
            for x in l:
                while k<len(r) and r[k]-x<lower:k+=1
                while j<len(r) and r[j]-x<=upper:j+=1
                ans+=j-k
            return sorted(l+r),ans
        return sort_count(p)[1]
