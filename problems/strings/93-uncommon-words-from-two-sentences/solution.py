class Solution:
    def uncommonFromSentences(self, s1: str, s2: str) -> List[str]:
        cnt = Counter(s1.split())
        cnt.update(s2.split())
        return [w for w, c in cnt.items() if c == 1]
