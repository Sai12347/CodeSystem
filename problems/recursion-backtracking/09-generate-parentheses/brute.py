from itertools import product


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        if n == 0:
            return [""]
        res: List[str] = []
        for chars in product("()", repeat=2 * n):
            bal = 0
            valid = True
            for ch in chars:
                bal += 1 if ch == "(" else -1
                if bal < 0:
                    valid = False
                    break
            if valid and bal == 0:
                res.append("".join(chars))
        return res
