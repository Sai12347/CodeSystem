class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        rank = [0] * 26
        for idx, ch in enumerate(order):
            rank[ord(ch) - 97] = idx
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            limit = min(len(w1), len(w2))
            differed = False
            for j in range(limit):
                r1 = rank[ord(w1[j]) - 97]
                r2 = rank[ord(w2[j]) - 97]
                if r1 != r2:
                    if r1 > r2:
                        return False
                    differed = True
                    break
            if not differed and len(w1) > len(w2):
                return False
        return True
