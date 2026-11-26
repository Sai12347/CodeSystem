class Solution:
    def rowWithMaximumOnes(self, mat: List[List[int]]) -> int:
        best_row, best_count = -1, 0
        for r, row in enumerate(mat):
            count = sum(row)
            if count > best_count: best_row, best_count = r, count
        return best_row
