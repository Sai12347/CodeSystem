class Solution:
    def canSortWithStack(self, perm: List[int]) -> bool:
        stack = []
        need = 1
        for x in perm:
            stack.append(x)
            while stack and stack[-1] == need:
                stack.pop()
                need += 1
        return need == len(perm) + 1
