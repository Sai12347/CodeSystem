class Solution:
    def minArea(self, image: List[List[str]], x: int, y: int) -> int:
        m, n = len(image), len(image[0])

        def row_has_one(r: int) -> bool:
            return '1' in image[r]

        def col_has_one(c: int) -> bool:
            for r in range(m):
                if image[r][c] == '1':
                    return True
            return False

        # Find top in [0, x]
        lo, hi = 0, x
        while lo < hi:
            mid = (lo + hi) // 2
            if row_has_one(mid):
                hi = mid
            else:
                lo = mid + 1
        top = lo

        # Find bottom in [x, m - 1]
        lo, hi = x, m - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if row_has_one(mid):
                lo = mid
            else:
                hi = mid - 1
        bottom = lo

        # Find left in [0, y]
        lo, hi = 0, y
        while lo < hi:
            mid = (lo + hi) // 2
            if col_has_one(mid):
                hi = mid
            else:
                lo = mid + 1
        left = lo

        # Find right in [y, n - 1]
        lo, hi = y, n - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if col_has_one(mid):
                lo = mid
            else:
                hi = mid - 1
        right = lo

        return (bottom - top + 1) * (right - left + 1)
