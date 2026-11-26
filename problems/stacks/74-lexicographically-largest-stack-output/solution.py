class Solution:
    def largestStackOutput(self, nums: List[int]) -> List[int]:
        n = len(nums)
        suf_max = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suf_max[i] = nums[i] if nums[i] > suf_max[i + 1] else suf_max[i + 1]
        stack = []
        out = []
        for i, x in enumerate(nums):
            stack.append(x)
            nxt_max = suf_max[i + 1]
            while stack and stack[-1] > nxt_max:
                out.append(stack.pop())
        return out
