class Solution:
    def spiralMatrixIII(self, rows: int, cols: int, rStart: int, cStart: int) -> List[List[int]]:
        total = rows * cols
        res = [[rStart, cStart]]
        dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
        r, c = rStart, cStart
        step = 1
        d = 0
        while len(res) < total:
            for _ in range(2):
                dr, dc = dirs[d]
                for _ in range(step):
                    r += dr
                    c += dc
                    if 0 <= r < rows and 0 <= c < cols:
                        res.append([r, c])
                        if len(res) == total:
                            return res
                d = (d + 1) & 3
            step += 1
        return res
