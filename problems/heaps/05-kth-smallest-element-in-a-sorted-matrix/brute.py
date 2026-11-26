class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        flat = [x for row in matrix for x in row]
        flat.sort()
        return flat[k - 1]
