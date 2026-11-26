class Solution:
    def countPartitions(self, nums: List[int], difference: int) -> int:
        total=sum(nums)
        if difference>total or (total+difference)%2:return 0
        target=(total+difference)//2;d=[0]*(target+1);d[0]=1
        for x in nums:
            for s in range(target,x-1,-1):d[s]+=d[s-x]
        return d[target]
