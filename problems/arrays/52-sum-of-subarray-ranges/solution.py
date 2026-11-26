class Solution:
    def sumSubarrayRanges(self, nums: List[int]) -> int:
        def contribution(is_min):
            stack = []
            total = 0
            for i in range(len(nums) + 1):
                while stack and (i == len(nums) or (nums[stack[-1]] >= nums[i] if is_min else nums[stack[-1]] <= nums[i])):
                    mid = stack.pop()
                    left = stack[-1] if stack else -1
                    total += nums[mid] * (mid - left) * (i - mid)
                stack.append(i)
            return total
        return contribution(False) - contribution(True)
