class Solution:
    def parseBoolExpr(self, expression: str) -> bool:
        stack = []
        for ch in expression:
            if ch == ',':
                continue
            if ch != ')':
                stack.append(ch)
            else:
                has_t = False
                has_f = False
                while stack[-1] != '(':
                    v = stack.pop()
                    if v == 't':
                        has_t = True
                    else:
                        has_f = True
                stack.pop()
                op = stack.pop()
                if op == '!':
                    res = 't' if has_f else 'f'
                elif op == '&':
                    res = 'f' if has_f else 't'
                else:
                    res = 't' if has_t else 'f'
                stack.append(res)
        return stack[-1] == 't'
