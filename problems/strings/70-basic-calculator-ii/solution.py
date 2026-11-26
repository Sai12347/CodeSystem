class Solution:
    def calculate(self, s: str) -> int:
        total = 0
        last = 0
        num = 0
        op = '+'
        n = len(s)
        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + (ord(ch) - 48)
            if (not ch.isdigit() and ch != ' ') or i == n - 1:
                if op == '+':
                    total += last
                    last = num
                elif op == '-':
                    total += last
                    last = -num
                elif op == '*':
                    last *= num
                else:
                    last = int(last / num)
                op = ch
                num = 0
        return total + last
