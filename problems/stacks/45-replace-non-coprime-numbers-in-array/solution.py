class Solution:
    def replaceNonCoprimes(self, nums: List[int]) -> List[int]:
        def gcd(a: int, b: int) -> int:
            while b:
                a, b = b, a % b
            return a

        stack = []
        for x in nums:
            cur = x
            while stack:
                g = gcd(stack[-1], cur)
                if g == 1:
                    break
                cur = (stack.pop() // g) * cur
            stack.append(cur)
        return stack
