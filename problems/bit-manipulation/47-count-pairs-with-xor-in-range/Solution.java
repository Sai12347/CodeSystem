class Solution {
    public int countPairsXorInRange(int[] nums, int low, int high) {
        return countLess(nums, high + 1) - countLess(nums, low);
    }

    private int countLess(int[] nums, int limit) {
        if (limit <= 0) return 0;
        final int MAX_BIT = 15;
        int maxNodes = nums.length * (MAX_BIT + 1) + 2;
        int[] c0 = new int[maxNodes];
        int[] c1 = new int[maxNodes];
        int[] cnt = new int[maxNodes];
        int nodes = 1;
        int total = 0;
        for (int x : nums) {
            int node = 0;
            for (int b = MAX_BIT; b >= 0; b--) {
                int xb = (x >> b) & 1;
                int lb = (limit >> b) & 1;
                if (lb == 1) {
                    int same = (xb == 1) ? c1[node] : c0[node];
                    if (same != 0) total += cnt[same];
                    node = (xb == 1) ? c0[node] : c1[node];
                } else {
                    node = (xb == 1) ? c1[node] : c0[node];
                }
                if (node == 0) break;
            }
            node = 0;
            for (int b = MAX_BIT; b >= 0; b--) {
                int xb = (x >> b) & 1;
                if (xb == 0) {
                    if (c0[node] == 0) c0[node] = nodes++;
                    node = c0[node];
                } else {
                    if (c1[node] == 0) c1[node] = nodes++;
                    node = c1[node];
                }
                cnt[node]++;
            }
        }
        return total;
    }
}
