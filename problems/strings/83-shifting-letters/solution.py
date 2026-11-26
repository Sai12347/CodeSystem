class Solution:
    def shiftingLetters(self, s: str, shifts: List[int]) -> str:
        n = len(s)
        chars = list(s)
        acc = 0
        for i in range(n - 1, -1, -1):
            acc = (acc + shifts[i]) % 26
            chars[i] = chr((ord(chars[i]) - 97 + acc) % 26 + 97)
        return "".join(chars)
