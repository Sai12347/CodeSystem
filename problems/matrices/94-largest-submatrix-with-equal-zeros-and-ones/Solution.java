class Solution {
    public int largestEqualZeroOneSubmatrix(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] g = grid;
        if (m > n) {
            g = new int[n][m];
            for (int r = 0; r < m; r++) {
                for (int c = 0; c < n; c++) g[c][r] = grid[r][c];
            }
            int tmp = m;
            m = n;
            n = tmp;
        }
        int best = 0;
        int[] col = new int[n];
        for (int r1 = 0; r1 < m; r1++) {
            Arrays.fill(col, 0);
            for (int r2 = r1; r2 < m; r2++) {
                int height = r2 - r1 + 1;
                int[] row = g[r2];
                int prefix = 0;
                Map<Integer, Integer> first = new HashMap<>();
                first.put(0, -1);
                for (int c = 0; c < n; c++) {
                    col[c] += (row[c] == 1) ? 1 : -1;
                    prefix += col[c];
                    Integer prev = first.get(prefix);
                    if (prev != null) {
                        int area = height * (c - prev);
                        if (area > best) best = area;
                    } else {
                        first.put(prefix, c);
                    }
                }
            }
        }
        return best;
    }
}
