class Solution {
    public int shortestPathBinaryMatrix(int[][] grid) {
        int n = grid.length;
        if (grid[0][0] != 0 || grid[n - 1][n - 1] != 0) {
            return -1;
        }
        if (n == 1) {
            return 1;
        }

        boolean[][] visited = new boolean[n][n];
        visited[0][0] = true;
        int[][] dirs = {
            {-1, -1}, {-1, 0}, {-1, 1},
            {0, -1},           {0, 1},
            {1, -1},  {1, 0},  {1, 1}
        };

        int[] qr = new int[n * n];
        int[] qc = new int[n * n];
        int[] qd = new int[n * n];
        int head = 0, tail = 0;
        qr[tail] = 0;
        qc[tail] = 0;
        qd[tail] = 1;
        tail++;

        while (head < tail) {
            int r = qr[head];
            int c = qc[head];
            int dist = qd[head];
            head++;
            int nd = dist + 1;
            for (int[] d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 0 && !visited[nr][nc]) {
                    if (nr == n - 1 && nc == n - 1) {
                        return nd;
                    }
                    visited[nr][nc] = true;
                    qr[tail] = nr;
                    qc[tail] = nc;
                    qd[tail] = nd;
                    tail++;
                }
            }
        }
        return -1;
    }
}
