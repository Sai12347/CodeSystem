class Solution {
    public List<List<Integer>> pacificAtlantic(int[][] heights) {
        List<List<Integer>> res = new ArrayList<>();
        if (heights == null || heights.length == 0 || heights[0].length == 0) {
            return res;
        }
        int rows = heights.length;
        int cols = heights[0].length;
        boolean[][] pac = new boolean[rows][cols];
        boolean[][] atl = new boolean[rows][cols];
        int[] qr = new int[rows * cols];
        int[] qc = new int[rows * cols];

        int head = 0, tail = 0;
        for (int c = 0; c < cols; c++) {
            if (!pac[0][c]) {
                pac[0][c] = true;
                qr[tail] = 0;
                qc[tail++] = c;
            }
        }
        for (int r = 0; r < rows; r++) {
            if (!pac[r][0]) {
                pac[r][0] = true;
                qr[tail] = r;
                qc[tail++] = 0;
            }
        }
        bfs(heights, pac, qr, qc, head, tail);

        head = 0;
        tail = 0;
        for (int c = 0; c < cols; c++) {
            if (!atl[rows - 1][c]) {
                atl[rows - 1][c] = true;
                qr[tail] = rows - 1;
                qc[tail++] = c;
            }
        }
        for (int r = 0; r < rows; r++) {
            if (!atl[r][cols - 1]) {
                atl[r][cols - 1] = true;
                qr[tail] = r;
                qc[tail++] = cols - 1;
            }
        }
        bfs(heights, atl, qr, qc, head, tail);

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (pac[r][c] && atl[r][c]) {
                    res.add(Arrays.asList(r, c));
                }
            }
        }
        return res;
    }

    private void bfs(int[][] heights, boolean[][] vis, int[] qr, int[] qc, int head, int tail) {
        int rows = heights.length;
        int cols = heights[0].length;
        while (head < tail) {
            int r = qr[head];
            int c = qc[head++];
            int h = heights[r][c];
            if (r > 0 && !vis[r - 1][c] && heights[r - 1][c] >= h) {
                vis[r - 1][c] = true;
                qr[tail] = r - 1;
                qc[tail++] = c;
            }
            if (r + 1 < rows && !vis[r + 1][c] && heights[r + 1][c] >= h) {
                vis[r + 1][c] = true;
                qr[tail] = r + 1;
                qc[tail++] = c;
            }
            if (c > 0 && !vis[r][c - 1] && heights[r][c - 1] >= h) {
                vis[r][c - 1] = true;
                qr[tail] = r;
                qc[tail++] = c - 1;
            }
            if (c + 1 < cols && !vis[r][c + 1] && heights[r][c + 1] >= h) {
                vis[r][c + 1] = true;
                qr[tail] = r;
                qc[tail++] = c + 1;
            }
        }
    }
}
