class Solution {
    public int largestAltitude(int[] gain) {
        int altitude = 0, best = 0;
        for (int x : gain) { altitude += x; best = Math.max(best, altitude); }
        return best;
    }
}
