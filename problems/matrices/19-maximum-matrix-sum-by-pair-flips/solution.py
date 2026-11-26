class Solution:
    def maxMatrixSum(self, matrix: List[List[int]]) -> int:
        total = 0
        smallest = float('inf')
        negatives = 0
        for row in matrix:
            for x in row:
                total += abs(x); smallest = min(smallest, abs(x)); negatives += x < 0
        return total - (2 * smallest if negatives % 2 else 0)
