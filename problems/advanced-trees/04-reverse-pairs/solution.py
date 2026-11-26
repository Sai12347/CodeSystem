class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        vals=sorted(set(nums));bit=[0]*(len(vals)+1);seen=ans=0
        def query(i):
            s=0
            while i:s+=bit[i];i-=i&-i
            return s
        for x in reversed(nums):
            k=bisect.bisect_right(vals,(x-1)//2);ans+=query(k);r=bisect.bisect_left(vals,x)+1
            while r<len(bit):bit[r]+=1;r+=r&-r
        return ans

