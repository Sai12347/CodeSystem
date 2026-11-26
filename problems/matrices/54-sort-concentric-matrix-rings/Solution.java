class Solution {
    public int[][] sortMatrixRings(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] res = new int[m][n];
        int top = 0, bottom = m - 1, left = 0, right = n - 1;
        while (top <= bottom && left <= right) {
            List<int[]> coords = new ArrayList<>();
            for (int c = left; c <= right; c++) coords.add(new int[]{top, c});
            for (int r = top + 1; r <= bottom; r++) coords.add(new int[]{r, right});
            if (bottom > top && right > left) {
                for (int c = right - 1; c >= left; c--) coords.add(new int[]{bottom, c});
                for (int r = bottom - 1; r > top; r--) coords.add(new int[]{r, left});
            }
            int sz = coords.size();
            int[] vals = new int[sz];
            for (int i = 0; i < sz; i++) {
                int[] p = coords.get(i);
                vals[i] = grid[p[0]][p[1]];
            }
            Arrays.sort(vals);
            for (int i = 0; i < sz; i++) {
                int[] p = coords.get(i);
                res[p[0]][p[1]] = vals[i];
            }
            top++;
            bottom--;
            left++;
            right--;
        }
        return res;
    }
}
