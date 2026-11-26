class Solution {
    public int maxMinDistance(int[] stalls, int cows) {
        Arrays.sort(stalls);
        int lo = 1;
        int hi = stalls[stalls.length - 1] - stalls[0];
        while (lo < hi) {
            int mid = lo + (hi - lo + 1) / 2;
            int placed = 1;
            int last = stalls[0];
            for (int i = 1; i < stalls.length; i++) {
                if (stalls[i] - last >= mid) {
                    placed++;
                    last = stalls[i];
                    if (placed == cows) {
                        break;
                    }
                }
            }
            if (placed >= cows) {
                lo = mid;
            } else {
                hi = mid - 1;
            }
        }
        return lo;
    }
}
