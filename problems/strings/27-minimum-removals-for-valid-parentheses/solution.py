class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        kept = []
        open_count = 0
        for c in s:
            if c == '(': open_count += 1; kept.append(c)
            elif c == ')':
                if open_count == 0: continue
                open_count -= 1; kept.append(c)
            else: kept.append(c)
        out = []
        for c in reversed(kept):
            if c == '(' and open_count: open_count -= 1
            else: out.append(c)
        return ''.join(reversed(out))
