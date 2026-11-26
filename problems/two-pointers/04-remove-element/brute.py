class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        kept = [x for x in nums if x != val]
        for i, x in enumerate(kept):
            nums[i] = x
        return len(kept)
