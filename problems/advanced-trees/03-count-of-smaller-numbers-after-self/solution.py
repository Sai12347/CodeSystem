class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        vals=sorted(set(nums)); bit=[0]*(len(vals)+1); out=[]
        def add(i):
            while i<len(bit):bit[i]+=1;i+=i&-i
        def query(i):
            s=0
            while i:s+=bit[i];i-=i&-i
            return s
        for x in reversed(nums):
            r=bisect.bisect_left(vals,x);out.append(query(r));add(r+1)
        return out[::-1]

