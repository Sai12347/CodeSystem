class Solution {
    public int[] gridIllumination(int n, int[][] lamps, int[][] queries) {
        Set<Long> active = new HashSet<>();
        Map<Integer, Integer> rows = new HashMap<>();
        Map<Integer, Integer> cols = new HashMap<>();
        Map<Integer, Integer> d1 = new HashMap<>();
        Map<Integer, Integer> d2 = new HashMap<>();
        for (int[] lamp : lamps) {
            int r = lamp[0], c = lamp[1];
            long key = (((long) r) << 32) | (c & 0xffffffffL);
            if (active.add(key)) {
                rows.merge(r, 1, Integer::sum);
                cols.merge(c, 1, Integer::sum);
                d1.merge(r - c, 1, Integer::sum);
                d2.merge(r + c, 1, Integer::sum);
            }
        }
        int[] ans = new int[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int qr = queries[i][0], qc = queries[i][1];
            if (rows.getOrDefault(qr, 0) > 0
                    || cols.getOrDefault(qc, 0) > 0
                    || d1.getOrDefault(qr - qc, 0) > 0
                    || d2.getOrDefault(qr + qc, 0) > 0) {
                ans[i] = 1;
            }
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    int nr = qr + dr, nc = qc + dc;
                    if (nr >= 0 && nr < n && nc >= 0 && nc < n) {
                        long key = (((long) nr) << 32) | (nc & 0xffffffffL);
                        if (active.remove(key)) {
                            rows.merge(nr, -1, Integer::sum);
                            cols.merge(nc, -1, Integer::sum);
                            d1.merge(nr - nc, -1, Integer::sum);
                            d2.merge(nr + nc, -1, Integer::sum);
                        }
                    }
                }
            }
        }
        return ans;
    }
}
