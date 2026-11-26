class Solution:
    def camelMatch(self, queries: List[str], pattern: str) -> List[bool]:
        def ok(q: str) -> bool:
            j = 0
            m = len(pattern)
            for ch in q:
                if j < m and ch == pattern[j]:
                    j += 1
                elif 'A' <= ch <= 'Z':
                    return False
            return j == m
        return [ok(q) for q in queries]
