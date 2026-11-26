class Solution:
    def regexLengthBounds(self, regex: str) -> List[int]:
        stack = []
        has_alt = False
        alt_min = 0
        alt_max = 0
        cur_min = 0
        cur_max = 0
        has_last = False
        last_min = 0
        last_max = 0

        i = 0
        n = len(regex)
        while i < n:
            ch = regex[i]
            if 'a' <= ch <= 'z':
                if has_last:
                    cur_min += last_min
                    cur_max += last_max
                has_last = True
                last_min = 1
                last_max = 1
                i += 1
            elif ch == '(':
                if has_last:
                    cur_min += last_min
                    cur_max += last_max
                    has_last = False
                stack.append((has_alt, alt_min, alt_max, cur_min, cur_max))
                has_alt = False
                alt_min = alt_max = cur_min = cur_max = 0
                i += 1
            elif ch == '|':
                if has_last:
                    cur_min += last_min
                    cur_max += last_max
                    has_last = False
                if not has_alt:
                    has_alt = True
                    alt_min, alt_max = cur_min, cur_max
                else:
                    if cur_min < alt_min:
                        alt_min = cur_min
                    if cur_max > alt_max:
                        alt_max = cur_max
                cur_min = cur_max = 0
                i += 1
            elif ch == ')':
                if has_last:
                    cur_min += last_min
                    cur_max += last_max
                    has_last = False
                if not has_alt:
                    g_min, g_max = cur_min, cur_max
                else:
                    g_min = cur_min if cur_min < alt_min else alt_min
                    g_max = cur_max if cur_max > alt_max else alt_max
                has_alt, alt_min, alt_max, cur_min, cur_max = stack.pop()
                has_last = True
                last_min, last_max = g_min, g_max
                i += 1
            elif ch == '?':
                last_min = 0
                i += 1
            elif ch == '{':
                j = regex.index('}', i)
                body = regex[i + 1:j]
                if ',' in body:
                    p1, p2 = body.split(',')
                    lo, hi = int(p1), int(p2)
                else:
                    lo = hi = int(body)
                last_min *= lo
                last_max *= hi
                i = j + 1
            else:
                i += 1

        if has_last:
            cur_min += last_min
            cur_max += last_max
        if not has_alt:
            return [cur_min, cur_max]
        return [min(alt_min, cur_min), max(alt_max, cur_max)]
