class Solution:
    def integerReplacement(self, n: int) -> int:
        x = n
        steps = 0
        while x > 1:
            if (x & 1) == 0:
                x >>= 1
            elif x == 3 or (x & 3) == 1:
                x -= 1
            else:
                x += 1
            steps += 1
        return steps
