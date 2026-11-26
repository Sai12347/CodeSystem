class Solution:
    def matchingBracketIndices(self, s: str) -> List[int]:
        n = len(s)
        ans = [-1] * n
        stack = []
        for i, ch in enumerate(s):
            if ch in '([{':
                stack.append(i)
            elif ch in ')]}':
                j = stack.pop()
                ans[i] = j
                ans[j] = i
        return ans
