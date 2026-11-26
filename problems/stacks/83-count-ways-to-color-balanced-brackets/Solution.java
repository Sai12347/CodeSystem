class Solution {
    public int countBracketColorings(String s) {
        final long MOD = 1_000_000_007L;
        int[][] validPairs = {{0, 1}, {0, 2}, {1, 0}, {2, 0}};
        List<long[][]> frames = new ArrayList<>();
        frames.add(null);
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                frames.add(null);
            } else {
                long[][] inner = frames.remove(frames.size() - 1);
                long[][] block = new long[3][3];
                if (inner == null) {
                    for (int[] p : validPairs) block[p[0]][p[1]] = 1L;
                } else {
                    for (int[] p : validPairs) {
                        int cl = p[0], cr = p[1];
                        long tot = 0;
                        for (int a = 0; a < 3; a++) {
                            if (cl != 0 && cl == a) continue;
                            for (int b = 0; b < 3; b++) {
                                if (cr != 0 && cr == b) continue;
                                tot += inner[a][b];
                            }
                        }
                        block[cl][cr] = tot % MOD;
                    }
                }
                int topIdx = frames.size() - 1;
                frames.set(topIdx, mergeTables(frames.get(topIdx), block, MOD));
            }
        }
        long[][] root = frames.get(0);
        long ans = 0;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                ans = (ans + root[i][j]) % MOD;
            }
        }
        return (int) ans;
    }

    private long[][] mergeTables(long[][] a, long[][] b, long MOD) {
        if (a == null) return b;
        long[][] res = new long[3][3];
        for (int l1 = 0; l1 < 3; l1++) {
            for (int r1 = 0; r1 < 3; r1++) {
                long va = a[l1][r1];
                if (va == 0) continue;
                for (int l2 = 0; l2 < 3; l2++) {
                    if (r1 != 0 && r1 == l2) continue;
                    for (int r2 = 0; r2 < 3; r2++) {
                        long vb = b[l2][r2];
                        if (vb != 0) {
                            res[l1][r2] = (res[l1][r2] + va * vb) % MOD;
                        }
                    }
                }
            }
        }
        return res;
    }
}
