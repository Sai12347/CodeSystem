class Solution {
    public long maximumWealth(int[][] accounts) {
        long best = 0;
        for (int[] row : accounts) { long sum = 0; for (int x : row) sum += x; best = Math.max(best, sum); }
        return best;
    }
}
