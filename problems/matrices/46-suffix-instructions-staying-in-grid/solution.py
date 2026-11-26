class Solution:
    def executeInstructions(self, n: int, startPos: List[int], s: str) -> List[int]:
        m = len(s)
        sr, sc = startPos[0], startPos[1]
        # Compute prefix displacements from index 0
        pr = [0] * (m + 1)
        pc = [0] * (m + 1)
        for i, ch in enumerate(s):
            dr = -1 if ch == 'U' else (1 if ch == 'D' else 0)
            dc = -1 if ch == 'L' else (1 if ch == 'R' else 0)
            pr[i + 1] = pr[i] + dr
            pc[i + 1] = pc[i] + dc

        ans = [0] * m
        row_seen = {}
        col_seen = {}
        for i in range(m - 1, -1, -1):
            row_seen[pr[i + 1]] = i + 1
            col_seen[pc[i + 1]] = i + 1
            stop = m + 1
            for target_r in (pr[i] - sr - 1, pr[i] + n - sr):
                if target_r in row_seen and row_seen[target_r] < stop:
                    stop = row_seen[target_r]
            for target_c in (pc[i] - sc - 1, pc[i] + n - sc):
                if target_c in col_seen and col_seen[target_c] < stop:
                    stop = col_seen[target_c]
            ans[i] = stop - 1 - i
        return ans
