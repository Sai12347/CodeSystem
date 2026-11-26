class Solution:
    def lengthLongestPath(self, input: str) -> int:
        stack = [0]
        best = 0
        for line in input.split('\n'):
            depth = 0
            while depth < len(line) and line[depth] == '\t':
                depth += 1
            name = line[depth:]
            while len(stack) > depth + 1:
                stack.pop()
            cur_len = stack[-1] + len(name)
            if '.' in name:
                if cur_len > best:
                    best = cur_len
            else:
                stack.append(cur_len + 1)
        return best
