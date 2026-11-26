class Solution:
    def totalRounds(self, nums: List[int]) -> int:
        stack = []
        ans = 0
        for x in nums:
            rounds = 0
            while stack and stack[-1][0] <= x:
                if stack[-1][1] > rounds:
                    rounds = stack[-1][1]
                stack.pop()
            if stack:
                rounds += 1
            else:
                rounds = 0
            if rounds > ans:
                ans = rounds
            stack.append((x, rounds))
        return ans
