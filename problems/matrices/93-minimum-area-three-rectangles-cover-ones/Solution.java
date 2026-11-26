class Solution {
    public int minimumSumThreeRectangles(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] ps = new int[m + 1][n + 1];
        for (int r = 0; r < m; r++) {
            int rowSum = 0;
            for (int c = 0; c < n; c++) {
                rowSum += grid[r][c];
                ps[r + 1][c + 1] = ps[r][c + 1] + rowSum;
            }
        }
        int INF = 1_000_000_000;
        int ans = INF;
        for (int r1 = 0; r1 < m - 2; r1++) {
            int a1 = bbox(ps, 0, r1, 0, n - 1, INF);
            if (a1 >= ans) continue;
            for (int r2 = r1 + 1; r2 < m - 1; r2++) {
                int a2 = bbox(ps, r1 + 1, r2, 0, n - 1, INF);
                int a3 = bbox(ps, r2 + 1, m - 1, 0, n - 1, INF);
                if (a2 < INF && a3 < INF) {
                    ans = Math.min(ans, a1 + a2 + a3);
                }
            }
        }
        for (int c1 = 0; c1 < n - 2; c1++) {
            int a1 = bbox(ps, 0, m - 1, 0, c1, INF);
            if (a1 >= ans) continue;
            for (int c2 = c1 + 1; c2 < n - 1; c2++) {
                int a2 = bbox(ps, 0, m - 1, c1 + 1, c2, INF);
                int a3 = bbox(ps, 0, m - 1, c2 + 1, n - 1, INF);
                if (a2 < INF && a3 < INF) {
                    ans = Math.min(ans, a1 + a2 + a3);
                }
            }
        }
        for (int r = 0; r < m - 1; r++) {
            int topFull = bbox(ps, 0, r, 0, n - 1, INF);
            int botFull = bbox(ps, r + 1, m - 1, 0, n - 1, INF);
            for (int c = 0; c < n - 1; c++) {
                int tl = bbox(ps, 0, r, 0, c, INF);
                int tr = bbox(ps, 0, r, c + 1, n - 1, INF);
                int bl = bbox(ps, r + 1, m - 1, 0, c, INF);
                int br = bbox(ps, r + 1, m - 1, c + 1, n - 1, INF);
                int leftFull = bbox(ps, 0, m - 1, 0, c, INF);
                int rightFull = bbox(ps, 0, m - 1, c + 1, n - 1, INF);
                if (topFull < INF && bl < INF && br < INF) ans = Math.min(ans, topFull + bl + br);
                if (tl < INF && tr < INF && botFull < INF) ans = Math.min(ans, tl + tr + botFull);
                if (leftFull < INF && tr < INF && br < INF) ans = Math.min(ans, leftFull + tr + br);
                if (tl < INF && bl < INF && rightFull < INF) ans = Math.min(ans, tl + bl + rightFull);
            }
        }
        return ans;
    }

    private int ones(int[][] ps, int r1, int r2, int c1, int c2) {
        return ps[r2 + 1][c2 + 1] - ps[r1][c2 + 1] - ps[r2 + 1][c1] + ps[r1][c1];
    }

    private int bbox(int[][] ps, int r1, int r2, int c1, int c2, int inf) {
        if (ones(ps, r1, r2, c1, c2) == 0) return inf;
        int top = r1;
        while (ones(ps, top, top, c1, c2) == 0) top++;
        int bot = r2;
        while (ones(ps, bot, bot, c1, c2) == 0) bot--;
        int left = c1;
        while (ones(ps, top, bot, left, left) == 0) left++;
        int right = c2;
        while (ones(ps, top, bot, right, right) == 0) right--;
        return (bot - top + 1) * (right - left + 1);
    }
}
