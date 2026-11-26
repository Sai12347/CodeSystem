class Solution:
    def minInsertions(self, s: str) -> int:
        insertions = 0
        opens = 0
        i = 0
        n = len(s)
        while i < n:
            if s[i] == '(':
                opens += 1
                i += 1
            else:
                if i + 1 < n and s[i + 1] == ')':
                    i += 2
                else:
                    insertions += 1
                    i += 1
                if opens > 0:
                    opens -= 1
                else:
                    insertions += 1
        return insertions + 2 * opens
