class Solution:
    def countOfAtoms(self, formula: str) -> str:
        stack = [{}]
        i = 0
        n = len(formula)
        while i < n:
            if formula[i] == '(':
                stack.append({})
                i += 1
            elif formula[i] == ')':
                i += 1
                mult = 0
                while i < n and formula[i].isdigit():
                    mult = mult * 10 + (ord(formula[i]) - 48)
                    i += 1
                mult = mult or 1
                top = stack.pop()
                cur = stack[-1]
                for atom, cnt in top.items():
                    cur[atom] = cur.get(atom, 0) + cnt * mult
            else:
                j = i + 1
                while j < n and formula[j].islower():
                    j += 1
                atom = formula[i:j]
                i = j
                cnt = 0
                while i < n and formula[i].isdigit():
                    cnt = cnt * 10 + (ord(formula[i]) - 48)
                    i += 1
                cnt = cnt or 1
                cur = stack[-1]
                cur[atom] = cur.get(atom, 0) + cnt
        parts = []
        for atom in sorted(stack[0]):
            cnt = stack[0][atom]
            parts.append(atom if cnt == 1 else f"{atom}{cnt}")
        return "".join(parts)
