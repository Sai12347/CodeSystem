class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # Coordinate-coverage sweep on [0..10000] using point + half-step markers
        max_coord = max(e for _, e in intervals)
        # Double coordinates: 2*x represents integer point x, 2*x+1 represents open segment (x, x+1)
        diff = [0] * (2 * max_coord + 3)
        for s, e in intervals:
            diff[2 * s] += 1
            diff[2 * e + 1] -= 1
        res = []
        cur = 0
        start = None
        for pos in range(2 * max_coord + 2):
            cur += diff[pos]
            if cur > 0 and start is None:
                start = pos // 2
            elif cur == 0 and start is not None:
                res.append([start, (pos - 1) // 2])
                start = None
        return res
