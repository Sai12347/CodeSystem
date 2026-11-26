class Solution {
    public int minOperationsToMakeContinuous(int[] nums) {
        int n = nums.length; int[] a = nums.clone(); Arrays.sort(a);
        int unique = 0; for (int x : a) if (unique == 0 || a[unique - 1] != x) a[unique++] = x;
        int best = 0, left = 0;
        for (int right = 0; right < unique; right++) { while ((long)a[right] - a[left] >= n) left++; best = Math.max(best, right - left + 1); }
        return n - best;
    }
}
