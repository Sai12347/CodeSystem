class Solution:
    def maxEqualRowsAfterFlips(self, matrix: List[List[int]]) -> int:
        counts = Counter()
        for row in matrix:
            first = row[0]
            pattern = tuple(v ^ first for v in row)
            counts[pattern] += 1
        return max(counts.values())
