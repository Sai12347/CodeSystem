class Solution:
    def isHappy(self, n: int) -> bool:
        def step(x: int) -> int:
            total = 0
            while x > 0:
                x, d = divmod(x, 10)
                total += d * d
            return total

        slow = n
        fast = step(n)
        while fast != 1 and slow != fast:
            slow = step(slow)
            fast = step(step(fast))
        return fast == 1
