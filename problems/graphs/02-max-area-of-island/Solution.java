class Solution {
    public int maxAreaOfIsland(int[][] grid) {
        if (grid == null || grid.length == 0 || grid[0].length == 0) {
            return 0;
        }
        int rows = grid.length;
        int cols = grid[0].length;
        int best = 0;
        int[] stackR = new int[rows * cols];
        int[] stackC = new int[rows * cols];

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] != 1) {
                    continue;
                }
                grid[r][c] = 0;
                int top = 0;
                stackR[top] = r;
                stackC[top] = c;
                top++;
                int area = 0;
                while (top > 0) {
                    top--;
                    int cr = stackR[top];
                    int cc = stackC[top];
                    area++;
                    if (cr > 0 && grid[cr - 1][cc] == 1) {
                        grid[cr - 1][cc] = 0;
                        stackR[top] = cr - 1;
                        stackC[top] = cc;
                        top++;
                    }
                    if (cr + 1 < rows && grid[cr + 1][cc] == 1) {
                        grid[cr + 1][cc] = 0;
                        stackR[top] = cr + 1;
                        stackC[top] = cc;
                        top++;
                    }
                    if (cc > 0 && grid[cr][cc - 1] == 1) {
                        grid[cr][cc - 1] = 0;
                        stackR[top] = cr;
                        stackC[top] = cc - 1;
                        top++;
                    }
                    if (cc + 1 < cols && grid[cr][cc + 1] == 1) {
                        grid[cr][cc + 1] = 0;
                        stackR[top] = cr;
                        stackC[top] = cc + 1;
                        top++;
                    }
                }
                if (area > best) {
                    best = area;
                }
            }
        }
        return best;
    }
}
