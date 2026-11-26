class Solution {
    public int shortestPathAllKeys(String[] grid) {
        int m = grid.length;
        int n = grid[0].length();
        int sr = 0, sc = 0, keyCount = 0;

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                char ch = grid[r].charAt(c);
                if (ch == '@') {
                    sr = r;
                    sc = c;
                } else if (ch >= 'a' && ch <= 'f') {
                    keyCount++;
                }
            }
        }

        int targetMask = (1 << keyCount) - 1;
        boolean[][][] visited = new boolean[m][n][1 << keyCount];
        visited[sr][sc][0] = true;

        ArrayDeque<int[]> q = new ArrayDeque<>();
        q.offer(new int[]{sr, sc, 0, 0});
        int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        while (!q.isEmpty()) {
            int[] cur = q.poll();
            int r = cur[0], c = cur[1], mask = cur[2], steps = cur[3];
            int ns = steps + 1;

            for (int[] d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr < 0 || nr >= m || nc < 0 || nc >= n) {
                    continue;
                }
                char ch = grid[nr].charAt(nc);
                if (ch == '#') {
                    continue;
                }
                if (ch >= 'A' && ch <= 'F' && (mask & (1 << (ch - 'A'))) == 0) {
                    continue;
                }
                int nmask = mask;
                if (ch >= 'a' && ch <= 'f') {
                    nmask |= (1 << (ch - 'a'));
                    if (nmask == targetMask) {
                        return ns;
                    }
                }
                if (!visited[nr][nc][nmask]) {
                    visited[nr][nc][nmask] = true;
                    q.offer(new int[]{nr, nc, nmask, ns});
                }
            }
        }
        return -1;
    }
}
