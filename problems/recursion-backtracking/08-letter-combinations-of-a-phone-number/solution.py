class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        keypad = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }
        res: List[str] = []
        path: List[str] = []
        n = len(digits)

        def dfs(idx: int) -> None:
            if idx == n:
                res.append("".join(path))
                return
            for ch in keypad[digits[idx]]:
                path.append(ch)
                dfs(idx + 1)
                path.pop()

        dfs(0)
        return res
