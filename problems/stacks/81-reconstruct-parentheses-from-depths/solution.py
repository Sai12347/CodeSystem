class Solution:
    def reconstructFromDepths(self, depths: List[int]) -> str:
        out = []
        open_cnt = 0
        for d in depths:
            if d == open_cnt + 1:
                open_cnt += 1
                out.append('(')
            elif open_cnt > 0 and d == open_cnt:
                open_cnt -= 1
                out.append(')')
            else:
                return ""
        return "".join(out) if open_cnt == 0 else ""
