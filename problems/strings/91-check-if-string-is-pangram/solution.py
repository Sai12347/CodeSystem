class Solution:
    def checkIfPangram(self, sentence: str) -> bool:
        mask = 0
        full = (1 << 26) - 1
        for ch in sentence:
            mask |= 1 << (ord(ch) - 97)
            if mask == full:
                return True
        return False
