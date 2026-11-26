class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res: List[str] = []
        buf: List[str] = []

        def backtrack(open_cnt: int, close_cnt: int) -> None:
            if len(buf) == 2 * n:
                res.append("".join(buf))
                return
            if open_cnt < n:
                buf.append("(")
                backtrack(open_cnt + 1, close_cnt)
                buf.pop()
            if close_cnt < open_cnt:
                buf.append(")")
                backtrack(open_cnt, close_cnt + 1)
                buf.pop()

        backtrack(0, 0)
        return res
