class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        open_cnt = 0
        adds = 0
        for ch in s:
            if ch == '(':
                open_cnt += 1
            elif open_cnt > 0:
                open_cnt -= 1
            else:
                adds += 1
        return adds + open_cnt
