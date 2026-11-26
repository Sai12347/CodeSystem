class Solution:
    def flipAndInvertImage(self, image: List[List[int]]) -> List[List[int]]:
        n = len(image)
        return [[1 - image[r][n - 1 - c] for c in range(n)] for r in range(n)]
