class Solution {
    public int[][] spiralMatrixIII(int rows, int cols, int rStart, int cStart) {
        int total = rows * cols;
        int[][] res = new int[total][2];
        int idx = 0;
        res[idx][0] = rStart;
        res[idx][1] = cStart;
        idx++;
        int[][] dirs = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
        int r = rStart, c = cStart, step = 1, d = 0;
        while (idx < total) {
            for (int rep = 0; rep < 2; rep++) {
                int dr = dirs[d][0], dc = dirs[d][1];
                for (int s = 0; s < step; s++) {
                    r += dr;
                    c += dc;
                    if (r >= 0 && r < rows && c >= 0 && c < cols) {
                        res[idx][0] = r;
                        res[idx][1] = c;
                        idx++;
                        if (idx == total) return res;
                    }
                }
                d = (d + 1) & 3;
            }
            step++;
        }
        return res;
    }
}
