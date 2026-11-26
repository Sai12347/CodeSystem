class Solution:
    def find132pattern(self, nums: List[int]) -> bool:
        stack = []
        third = -math.inf
        for i in range(len(nums) - 1, -1, -1):
            val = nums[i]
            if val < third:
                return True
            while stack and stack[-1] < val:
                third = stack.pop()
            stack.append(val)
        return False
