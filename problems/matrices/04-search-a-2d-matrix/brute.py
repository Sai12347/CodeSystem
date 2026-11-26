class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        return any(val == target for row in matrix for val in row)
