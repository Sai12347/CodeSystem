class Solution {
    public long maximumThreeRooksSum(int[][] board) {
        int m = board.length, n = board[0].length;
        int[][][] rows = new int[m][3][2];
        for (int r = 0; r < m; r++) {
            rows[r] = rowTop3(board[r]);
        }
        int[][][] pref = new int[m][][];
        pref[0] = rows[0];
        for (int r = 1; r < m; r++) {
            pref[r] = mergeTop3(pref[r - 1], rows[r]);
        }
        int[][][] suff = new int[m][][];
        suff[m - 1] = rows[m - 1];
        for (int r = m - 2; r >= 0; r--) {
            suff[r] = mergeTop3(suff[r + 1], rows[r]);
        }
        long ans = Long.MIN_VALUE;
        for (int r = 1; r < m - 1; r++) {
            int[][] pList = pref[r - 1];
            int[][] curList = rows[r];
            int[][] sList = suff[r + 1];
            for (int[] p : pList) {
                for (int[] cur : curList) {
                    if (p[1] == cur[1]) continue;
                    for (int[] s : sList) {
                        if (s[1] == p[1] || s[1] == cur[1]) continue;
                        long sum = (long) p[0] + cur[0] + s[0];
                        if (sum > ans) ans = sum;
                    }
                }
            }
        }
        return ans;
    }

    private int[][] rowTop3(int[] row) {
        int[][] top = {{Integer.MIN_VALUE, -1}, {Integer.MIN_VALUE, -1}, {Integer.MIN_VALUE, -1}};
        for (int c = 0; c < row.length; c++) {
            int v = row[c];
            if (v > top[0][0]) {
                top[2] = top[1];
                top[1] = top[0];
                top[0] = new int[]{v, c};
            } else if (v > top[1][0]) {
                top[2] = top[1];
                top[1] = new int[]{v, c};
            } else if (v > top[2][0]) {
                top[2] = new int[]{v, c};
            }
        }
        return top;
    }

    private int[][] mergeTop3(int[][] a, int[][] b) {
        int[][] combined = new int[6][2];
        int size = 0;
        for (int[] item : a) {
            size = insertColMax(combined, size, item[0], item[1]);
        }
        for (int[] item : b) {
            size = insertColMax(combined, size, item[0], item[1]);
        }
        Arrays.sort(combined, 0, size, (x, y) -> Integer.compare(y[0], x[0]));
        int[][] res = new int[3][2];
        for (int i = 0; i < 3; i++) {
            res[i] = new int[]{combined[i][0], combined[i][1]};
        }
        return res;
    }

    private int insertColMax(int[][] arr, int size, int v, int c) {
        for (int i = 0; i < size; i++) {
            if (arr[i][1] == c) {
                if (v > arr[i][0]) arr[i][0] = v;
                return size;
            }
        }
        arr[size][0] = v;
        arr[size][1] = c;
        return size + 1;
    }
}
