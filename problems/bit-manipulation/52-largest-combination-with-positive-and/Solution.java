class Solution {
    public int largestCombination(int[] candidates) {
        int best = 0;
        for (int b = 0; b < 24; b++) {
            int mask = 1 << b;
            int cnt = 0;
            for (int x : candidates) {
                if ((x & mask) != 0) cnt++;
            }
            if (cnt > best) best = cnt;
        }
        return best;
    }
}
