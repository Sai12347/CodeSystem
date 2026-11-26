class Solution {
    public boolean findRotation(int[][] mat, int[][] target) {
        int n = mat.length;
        boolean ok0 = true, ok90 = true, ok180 = true, ok270 = true;
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                int v = mat[r][c];
                if (v != target[r][c]) ok0 = false;
                if (v != target[c][n - 1 - r]) ok90 = false;
                if (v != target[n - 1 - r][n - 1 - c]) ok180 = false;
                if (v != target[n - 1 - c][r]) ok270 = false;
            }
        }
        return ok0 || ok90 || ok180 || ok270;
    }
}
