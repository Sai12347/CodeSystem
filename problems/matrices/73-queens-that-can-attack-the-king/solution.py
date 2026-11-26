class Solution:
    def queensAttackTheKing(self, n: int, queens: List[List[int]], king: List[int]) -> List[List[int]]:
        has_q = [[False] * n for _ in range(n)]
        for r, c in queens:
            has_q[r][c] = True
        kr, kc = king[0], king[1]
        res = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = kr + dr, kc + dc
                while 0 <= r < n and 0 <= c < n:
                    if has_q[r][c]:
                        res.append([r, c])
                        break
                    r += dr
                    c += dc
        res.sort()
        return res
