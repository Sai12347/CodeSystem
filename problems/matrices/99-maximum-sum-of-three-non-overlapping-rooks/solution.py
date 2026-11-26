class Solution:
    def maximumThreeRooksSum(self, board: List[List[int]]) -> int:
        m, n = len(board), len(board[0])

        def row_top3(row):
            top = []
            for c, v in enumerate(row):
                if len(top) < 3 or v > top[-1][0]:
                    top.append((v, c))
                    top.sort(key=lambda x: x[0], reverse=True)
                    if len(top) > 3:
                        top.pop()
            return top

        def merge_top3(a, b):
            best_by_col = {}
            for v, c in a:
                if c not in best_by_col or v > best_by_col[c]:
                    best_by_col[c] = v
            for v, c in b:
                if c not in best_by_col or v > best_by_col[c]:
                    best_by_col[c] = v
            items = sorted(((v, c) for c, v in best_by_col.items()), reverse=True)
            return items[:3]

        rows = [row_top3(board[r]) for r in range(m)]
        pref = [None] * m
        pref[0] = rows[0]
        for r in range(1, m):
            pref[r] = merge_top3(pref[r - 1], rows[r])

        suff = [None] * m
        suff[m - 1] = rows[m - 1]
        for r in range(m - 2, -1, -1):
            suff[r] = merge_top3(suff[r + 1], rows[r])

        ans = -10**18
        for r in range(1, m - 1):
            p_list = pref[r - 1]
            cur_list = rows[r]
            s_list = suff[r + 1]
            for v1, c1 in p_list:
                for v2, c2 in cur_list:
                    if c1 == c2:
                        continue
                    for v3, c3 in s_list:
                        if c3 == c1 or c3 == c2:
                            continue
                        total = v1 + v2 + v3
                        if total > ans:
                            ans = total
        return ans
