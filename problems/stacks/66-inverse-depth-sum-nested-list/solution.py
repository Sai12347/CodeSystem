class Solution:
    def inverseDepthSum(self, s: str) -> int:
        stack = []
        plain_sum = 0
        depth_sum = 0
        max_depth = 0
        i = 0
        n = len(s)
        while i < n:
            ch = s[i]
            if ch == '[':
                stack.append('[')
                i += 1
            elif ch == ']':
                stack.pop()
                i += 1
            elif ch == ',':
                i += 1
            else:
                sign = 1
                if ch == '-':
                    sign = -1
                    i += 1
                val = 0
                while i < n and s[i].isdigit():
                    val = val * 10 + (ord(s[i]) - 48)
                    i += 1
                val *= sign
                d = len(stack)
                if d > max_depth:
                    max_depth = d
                plain_sum += val
                depth_sum += val * d
        return (max_depth + 1) * plain_sum - depth_sum
