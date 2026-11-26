class Solution:
    def snakeTraverse(self, matrix: List[List[int]]) -> List[int]:
        res = []
        for r, row in enumerate(matrix):
            if r % 2 == 0:
                res.extend(row)
            else:
                res.extend(reversed(row))
        return res
