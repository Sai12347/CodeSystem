class Solution:
    def getMaximumConsecutive(self, coins: List[int]) -> int:
        reach = 0
        for coin in sorted(coins):
            if coin > reach + 1: break
            reach += coin
        return reach
