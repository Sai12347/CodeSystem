class Solution:
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:
        stack = []
        j = 0
        n = len(popped)
        for val in pushed:
            stack.append(val)
            while stack and j < n and stack[-1] == popped[j]:
                stack.pop()
                j += 1
        return j == n
