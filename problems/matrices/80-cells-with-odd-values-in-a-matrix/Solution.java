class Solution {
    public int oddCells(int m, int n, int[][] indices) {
        boolean[] rowOdd = new boolean[m];
        boolean[] colOdd = new boolean[n];
        for (int[] idx : indices) {
            rowOdd[idx[0]] = !rowOdd[idx[0]];
            colOdd[idx[1]] = !colOdd[idx[1]];
        }
        int ro = 0, co = 0;
        for (boolean b : rowOdd) if (b) ro++;
        for (boolean b : colOdd) if (b) co++;
        return ro * (n - co) + (m - ro) * co;
    }
}
