class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        words = set(wordDict)
        n = len(s)
        res: List[str] = []
        path: List[str] = []

        def backtrack(start: int) -> None:
            if start == n:
                res.append(" ".join(path))
                return
            for end in range(start + 1, n + 1):
                w = s[start:end]
                if w in words:
                    path.append(w)
                    backtrack(end)
                    path.pop()

        backtrack(0)
        return res
