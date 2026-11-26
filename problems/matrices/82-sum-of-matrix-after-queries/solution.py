class Solution:
    def matrixSumQueries(self, n: int, queries: List[List[int]]) -> int:
        seen_r = [False] * n
        seen_c = [False] * n
        rem_r = n
        rem_c = n
        total = 0
        for qtype, idx, val in reversed(queries):
            if qtype == 0:
                if not seen_r[idx]:
                    seen_r[idx] = True
                    total += val * rem_c
                    rem_r -= 1
            else:
                if not seen_c[idx]:
                    seen_c[idx] = True
                    total += val * rem_r
                    rem_c -= 1
            if rem_r == 0 or rem_c == 0:
                break
        return total
