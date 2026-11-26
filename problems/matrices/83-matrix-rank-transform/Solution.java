class Solution {
    public int[][] matrixRankTransform(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        TreeMap<Integer, List<int[]>> groups = new TreeMap<>();
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                groups.computeIfAbsent(matrix[r][c], k -> new ArrayList<>()).add(new int[]{r, c});
            }
        }
        int[] rowMax = new int[m];
        int[] colMax = new int[n];
        int[][] ans = new int[m][n];
        int[] parent = new int[m + n];
        int[] compRank = new int[m + n];

        for (List<int[]> cells : groups.values()) {
            for (int[] cell : cells) {
                int r = cell[0], cc = m + cell[1];
                parent[r] = r;
                parent[cc] = cc;
                compRank[r] = 0;
                compRank[cc] = 0;
            }
            for (int[] cell : cells) {
                int ra = find(parent, cell[0]);
                int rb = find(parent, m + cell[1]);
                if (ra != rb) parent[ra] = rb;
            }
            for (int[] cell : cells) {
                int r = cell[0], c = cell[1];
                int root = find(parent, r);
                int prev = Math.max(rowMax[r], colMax[c]);
                if (prev > compRank[root]) compRank[root] = prev;
            }
            for (int[] cell : cells) {
                int r = cell[0], c = cell[1];
                int rank = compRank[find(parent, r)] + 1;
                ans[r][c] = rank;
                rowMax[r] = rank;
                colMax[c] = rank;
            }
        }
        return ans;
    }

    private int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }
}
