class Solution {
    public int maxEqualRowsAfterFlips(int[][] matrix) {
        Map<String, Integer> counts = new HashMap<>();
        int best = 0;
        for (int[] row : matrix) {
            int first = row[0];
            char[] key = new char[row.length];
            for (int c = 0; c < row.length; c++) {
                key[c] = (row[c] == first) ? '0' : '1';
            }
            String s = new String(key);
            int cnt = counts.getOrDefault(s, 0) + 1;
            counts.put(s, cnt);
            if (cnt > best) best = cnt;
        }
        return best;
    }
}
