class Solution:
    def countRecordBreakers(self, nums: List[int]) -> int:
        count = 0
        high = None
        for x in nums:
            if high is None or x > high:
                count += 1
                high = x
        return count
