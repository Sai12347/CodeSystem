class Solution {
    public int countEqualXorTriplets(int[] arr) {
        Map<Integer, Integer> cnt = new HashMap<>();
        Map<Integer, Long> idxSum = new HashMap<>();
        cnt.put(0, 1);
        idxSum.put(0, 0L);
        int pref = 0;
        long ans = 0;
        for (int m = 1; m <= arr.length; m++) {
            pref ^= arr[m - 1];
            int c = cnt.getOrDefault(pref, 0);
            long s = idxSum.getOrDefault(pref, 0L);
            if (c > 0) {
                ans += (long) c * (m - 1) - s;
            }
            cnt.put(pref, c + 1);
            idxSum.put(pref, s + m);
        }
        return (int) ans;
    }
}
