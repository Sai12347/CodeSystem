class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        cand = 0
        count = 0
        for x in nums:
            if count == 0:
                cand = x
                count = 1
            elif x == cand:
                count += 1
            else:
                count -= 1
        return cand
