class Solution {
    public char[][] rotateTheBox(char[][] box) {
        int m = box.length, n = box[0].length;
        char[][] res = new char[n][m];
        for (int i = 0; i < n; i++) Arrays.fill(res[i], '.');
        for (int r = 0; r < m; r++) {
            int destCol = m - 1 - r;
            int write = n - 1;
            for (int c = n - 1; c >= 0; c--) {
                char ch = box[r][c];
                if (ch == '*') {
                    res[c][destCol] = '*';
                    write = c - 1;
                } else if (ch == '#') {
                    res[write][destCol] = '#';
                    write--;
                }
            }
        }
        return res;
    }
}
