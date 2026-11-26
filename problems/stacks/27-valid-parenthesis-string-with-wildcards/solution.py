class Solution:
    def checkValidString(self, s: str) -> bool:
        opens = []
        stars = []
        for i, ch in enumerate(s):
            if ch == '(':
                opens.append(i)
            elif ch == '*':
                stars.append(i)
            else:
                if opens:
                    opens.pop()
                elif stars:
                    stars.pop()
                else:
                    return False
        while opens and stars:
            if opens[-1] < stars[-1]:
                opens.pop()
                stars.pop()
            else:
                return False
        return not opens
