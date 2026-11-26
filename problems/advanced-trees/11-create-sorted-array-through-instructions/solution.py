class Solution:
    def createSortedArray(self, instructions: List[int]) -> int:
        mod=10**9+7; bit=[0]*(max(instructions)+1); total=0
        def query(i):
            s=0
            while i:s+=bit[i];i-=i&-i
            return s
        for i,x in enumerate(instructions):
            less=query(x-1); greater=i-query(x)
            total=(total+min(less,greater))%mod
            j=x
            while j<len(bit):bit[j]+=1;j+=j&-j
        return total
