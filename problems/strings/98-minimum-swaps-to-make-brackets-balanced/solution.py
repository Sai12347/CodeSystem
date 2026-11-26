class Solution:
    def minSwapsBalanced(self, s: str) -> int:
        close = 0
        max_close = 0
        for ch in s:
            if ch == '[':
                close -= 1
            else:
                close += 1
                if close > max_close:
                    max_close = close
        return (max_close + 1) // 2
