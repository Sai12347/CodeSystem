class Solution {
    public char[][] updateBoard(char[][] board, int[] click) {
        int m = board.length, n = board[0].length;
        char[][] res = new char[m][n];
        for (int r = 0; r < m; r++) res[r] = board[r].clone();
        int sr = click[0], sc = click[1];
        if (res[sr][sc] == 'M') {
            res[sr][sc] = 'X';
            return res;
        }
        boolean[][] visited = new boolean[m][n];
        ArrayDeque<int[]> q = new ArrayDeque<>();
        q.add(new int[]{sr, sc});
        visited[sr][sc] = true;
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            int r = cur[0], c = cur[1];
            int mines = 0;
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    if (dr == 0 && dc == 0) continue;
                    int nr = r + dr, nc = c + dc;
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n && res[nr][nc] == 'M') {
                        mines++;
                    }
                }
            }
            if (mines > 0) {
                res[r][c] = (char) ('0' + mines);
            } else {
                res[r][c] = 'B';
                for (int dr = -1; dr <= 1; dr++) {
                    for (int dc = -1; dc <= 1; dc++) {
                        if (dr == 0 && dc == 0) continue;
                        int nr = r + dr, nc = c + dc;
                        if (nr >= 0 && nr < m && nc >= 0 && nc < n && !visited[nr][nc] && res[nr][nc] == 'E') {
                            visited[nr][nc] = true;
                            q.add(new int[]{nr, nc});
                        }
                    }
                }
            }
        }
        return res;
    }
}
