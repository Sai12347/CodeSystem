class Solution:
    def luckyNumbers(self, matrix: List[List[int]]) -> List[int]:
        rowmins=[min(row) for row in matrix]
        colmax=[max(col) for col in zip(*matrix)]
        return [v for i,row in enumerate(matrix) for j,v in enumerate(row) if v==rowmins[i] and v==colmax[j]]
