class Solution:
    def longestSubarrayAtMostK(self, nums: List[int], k: int) -> int:
        left=total=best=0
        for right,x in enumerate(nums):
            total+=x
            while total>k: total-=nums[left];left+=1
            best=max(best,right-left+1)
        return best
