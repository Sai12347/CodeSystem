class Solution:
    def maximumGain(self, s: str, x: int, y: int) -> int:
        def remove_pair(text: str, first: str, second: str, pts: int):
            stack = []
            gain = 0
            for ch in text:
                if stack and stack[-1] == first and ch == second:
                    stack.pop()
                    gain += pts
                else:
                    stack.append(ch)
            return "".join(stack), gain

        if x >= y:
            rem, g1 = remove_pair(s, 'a', 'b', x)
            _, g2 = remove_pair(rem, 'b', 'a', y)
        else:
            rem, g1 = remove_pair(s, 'b', 'a', y)
            _, g2 = remove_pair(rem, 'a', 'b', x)
        return g1 + g2
