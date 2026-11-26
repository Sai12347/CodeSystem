class Solution {
    public long largestSumAfterKNegations(int[] nums, int k) {
        int[] a = nums.clone(); Arrays.sort(a);
        for (int i = 0; i < a.length && k > 0 && a[i] < 0; i++, k--) a[i] = -a[i];
        long sum = 0; int min = Integer.MAX_VALUE; for (int x : a) { sum += x; min = Math.min(min, x); }
        return (k & 1) == 1 ? sum - 2L * min : sum;
    }
}
