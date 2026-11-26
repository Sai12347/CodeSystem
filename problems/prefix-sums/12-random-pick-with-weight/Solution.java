class Solution {
    private final int[] prefix;
    private final int total;
    private final Random rng;

    public Solution(int[] w) {
        prefix = new int[w.length];
        int running = 0;
        for (int i = 0; i < w.length; i++) {
            running += w[i];
            prefix[i] = running;
        }
        total = running;
        rng = new Random();
    }

    public int pickIndex() {
        int target = rng.nextInt(total) + 1;
        int lo = 0, hi = prefix.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (prefix[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        return lo;
    }
}
