class Solution {
    public int[][] queensAttackTheKing(int n, int[][] queens, int[] king) {
        boolean[][] hasQ = new boolean[n][n];
        for (int[] q : queens) hasQ[q[0]][q[1]] = true;
        int kr = king[0], kc = king[1];
        List<int[]> res = new ArrayList<>();
        for (int dr = -1; dr <= 1; dr++) {
            for (int dc = -1; dc <= 1; dc++) {
                if (dr == 0 && dc == 0) continue;
                int r = kr + dr, c = kc + dc;
                while (r >= 0 && r < n && c >= 0 && c < n) {
                    if (hasQ[r][c]) {
                        res.add(new int[]{r, c});
                        break;
                    }
                    r += dr;
                    c += dc;
                }
            }
        }
        res.sort((a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        return res.toArray(new int[0][]);
    }
}
