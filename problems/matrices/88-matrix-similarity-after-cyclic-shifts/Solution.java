class Solution {
    public boolean areSimilarAfterShifts(int[][] mat, int k) {
        int n = mat[0].length;
        int shift = k % n;
        if (shift == 0) return true;
        for (int[] row : mat) {
            for (int c = 0; c < n; c++) {
                if (row[c] != row[(c + shift) % n]) {
                    return false;
                }
            }
        }
        return true;
    }
}
