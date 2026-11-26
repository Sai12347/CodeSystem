class Solution:
    def maxWordLengthProduct(self, words: List[str]) -> int:
        best_len = {}
        for w in words:
            mask = 0
            for ch in w:
                mask |= 1 << (ord(ch) - 97)
            if len(w) > best_len.get(mask, 0):
                best_len[mask] = len(w)
        items = list(best_len.items())
        ans = 0
        for i in range(len(items)):
            m1, l1 = items[i]
            for j in range(i + 1, len(items)):
                m2, l2 = items[j]
                if (m1 & m2) == 0 and l1 * l2 > ans:
                    ans = l1 * l2
        return ans
