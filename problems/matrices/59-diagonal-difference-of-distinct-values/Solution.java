class Solution {
    public int[][] differenceOfDistinctValues(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] ans = new int[m][n];
        for (int start = -(m - 1); start <= n - 1; start++) {
            int r = Math.max(0, -start);
            int c = Math.max(0, start);
            List<int[]> cells = new ArrayList<>();
            Set<Integer> seen = new HashSet<>();
            while (r < m && c < n) {
                ans[r][c] = seen.size();
                seen.add(grid[r][c]);
                cells.add(new int[]{r, c});
                r++;
                c++;
            }
            seen.clear();
            for (int i = cells.size() - 1; i >= 0; i--) {
                int cr = cells.get(i)[0], cc = cells.get(i)[1];
                ans[cr][cc] = Math.abs(ans[cr][cc] - seen.size());
                seen.add(grid[cr][cc]);
            }
        }
        return ans;
    }
}
