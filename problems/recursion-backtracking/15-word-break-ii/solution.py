class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        words = set(wordDict)
        n = len(s)
        max_len = max((len(w) for w in words), default=0)
        memo: dict[int, List[str]] = {}

        def dfs(start: int) -> List[str]:
            if start in memo:
                return memo[start]
            if start == n:
                return [""]
            res: List[str] = []
            limit = min(n, start + max_len)
            for end in range(start + 1, limit + 1):
                w = s[start:end]
                if w in words:
                    for tail in dfs(end):
                        res.append(w if not tail else f"{w} {tail}")
            memo[start] = res
            return res

        return dfs(0)
