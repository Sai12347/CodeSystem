class Solution:
    def areSimilarAfterShifts(self, mat: List[List[int]], k: int) -> bool:
        n = len(mat[0])
        shift = k % n
        if shift == 0:
            return True
        for row in mat:
            for c in range(n):
                if row[c] != row[(c + shift) % n]:
                    return False
        return True
