class Solution:
    def kthSpiralCell(self, rows: int, cols: int, k: int) -> List[int]:
        lo, hi = 0, (min(rows, cols) - 1) // 2
        total = rows * cols
        while lo < hi:
            mid = (lo + hi + 1) // 2
            consumed = total - (rows - 2 * mid) * (cols - 2 * mid)
            if consumed < k:
                lo = mid
            else:
                hi = mid - 1
        layer = lo
        consumed = total - (rows - 2 * layer) * (cols - 2 * layer)
        rem = k - 1 - consumed
        top, bottom = layer, rows - 1 - layer
        left, right = layer, cols - 1 - layer
        w = right - left + 1
        h = bottom - top + 1
        if rem < w:
            return [top, left + rem]
        rem -= w
        if rem < h - 1:
            return [top + 1 + rem, right]
        rem -= h - 1
        if rem < w - 1:
            return [bottom, right - 1 - rem]
        rem -= w - 1
        return [bottom - 1 - rem, left]
