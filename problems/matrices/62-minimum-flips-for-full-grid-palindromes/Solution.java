class Solution {
    public int minFlipsFullPalindrome(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int flips = 0;
        for (int r = 0; r < m / 2; r++) {
            for (int c = 0; c < n / 2; c++) {
                int ones = grid[r][c]
                        + grid[r][n - 1 - c]
                        + grid[m - 1 - r][c]
                        + grid[m - 1 - r][n - 1 - c];
                flips += Math.min(ones, 4 - ones);
            }
        }
        int diff = 0, pairOnes = 0;
        if (m % 2 == 1) {
            int mr = m / 2;
            for (int c = 0; c < n / 2; c++) {
                int a = grid[mr][c], b = grid[mr][n - 1 - c];
                if (a != b) diff++;
                else if (a == 1) pairOnes++;
            }
        }
        if (n % 2 == 1) {
            int mc = n / 2;
            for (int r = 0; r < m / 2; r++) {
                int a = grid[r][mc], b = grid[m - 1 - r][mc];
                if (a != b) diff++;
                else if (a == 1) pairOnes++;
            }
        }
        if (m % 2 == 1 && n % 2 == 1 && grid[m / 2][n / 2] == 1) {
            flips++;
        }
        flips += diff;
        if (pairOnes % 2 == 1 && diff == 0) {
            flips += 2;
        }
        return flips;
    }
}
