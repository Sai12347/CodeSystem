class Solution:
    def braceExpansion(self, expression: str) -> List[str]:
        stack = []
        union_set = set()
        cur_set = {""}
        for ch in expression:
            if ch == '{':
                stack.append((union_set, cur_set))
                union_set = set()
                cur_set = {""}
            elif ch == ',':
                union_set |= cur_set
                cur_set = {""}
            elif ch == '}':
                union_set |= cur_set
                prev_union, prev_cur = stack.pop()
                cur_set = {a + b for a in prev_cur for b in union_set}
                union_set = prev_union
            else:
                cur_set = {a + ch for a in cur_set}
        return sorted(union_set | cur_set)
