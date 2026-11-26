class Solution {
    public long matrixSumQueries(int n, int[][] queries) {
        boolean[] seenR = new boolean[n];
        boolean[] seenC = new boolean[n];
        int remR = n, remC = n;
        long total = 0;
        for (int i = queries.length - 1; i >= 0; i--) {
            int type = queries[i][0];
            int idx = queries[i][1];
            long val = queries[i][2];
            if (type == 0) {
                if (!seenR[idx]) {
                    seenR[idx] = true;
                    total += val * remC;
                    remR--;
                }
            } else {
                if (!seenC[idx]) {
                    seenC[idx] = true;
                    total += val * remR;
                    remC--;
                }
            }
            if (remR == 0 || remC == 0) break;
        }
        return total;
    }
}
