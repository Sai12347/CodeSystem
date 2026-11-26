class Solution {
    public int leftmostColumnWithOne(int[][] mat) {
        int m = mat.length, n = mat[0].length;
        int r = 0, c = n - 1, ans = -1;
        while (r < m && c >= 0) {
            if (mat[r][c] == 1) {
                ans = c;
                c--;
            } else {
                r++;
            }
        }
        return ans;
    }
}
