class Solution:
    def reverseOnlyLetters(self, s: str) -> str:
        letters = [ch for ch in s if ch.isalpha()]
        out = []
        for ch in s:
            if ch.isalpha():
                out.append(letters.pop())
            else:
                out.append(ch)
        return "".join(out)
