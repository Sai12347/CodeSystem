class Solution {
    public int[] findBall(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[] ans = new int[n];
        for (int start = 0; start < n; start++) {
            int col = start;
            for (int r = 0; r < m; r++) {
                int d = grid[r][col];
                int nxt = col + d;
                if (nxt < 0 || nxt >= n || grid[r][nxt] != d) {
                    col = -1;
                    break;
                }
                col = nxt;
            }
            ans[start] = col;
        }
        return ans;
    }
}
