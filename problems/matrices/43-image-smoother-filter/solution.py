class Solution:
    def imageSmoother(self, img: List[List[int]]) -> List[List[int]]:
        m, n = len(img), len(img[0])
        res = [[0] * n for _ in range(m)]
        for r in range(m):
            r0, r1 = max(0, r - 1), min(m - 1, r + 1)
            for c in range(n):
                c0, c1 = max(0, c - 1), min(n - 1, c + 1)
                total = 0
                cnt = 0
                for nr in range(r0, r1 + 1):
                    row = img[nr]
                    for nc in range(c0, c1 + 1):
                        total += row[nc]
                        cnt += 1
                res[r][c] = total // cnt
        return res
